# -*- coding: utf-8 -*-
"""
Created on Wed Dec 21 14:08:19 2022

@author: solis
varias funciones para cambiar el formato de un fichero de datos de meteoros
diarios con contenido codigo,fecha,valor a otro formato con contenido
codigo,año,mes,valores diarios del meteoro en el mes

LA ÚNICA FUNCIÓN PÚBLICA QUE ESTÁ TERMIANDA es pdia_2_array_variable_len. 
Escribe un nuevo fichero apto para importar los datos a una tabla de Postgres 
en que los valores diarios se guardan como un array de valores int2. 
Detalles en la función.

"""
from calendar import isleap
import csv
from datetime import datetime

DAYS_IN_MONTH = 31
NODATA = '_%_'


def _init_v_variable_len(line: list):
    """
    Inicialización de variables
    El número de elementos en d_values es el del número de días del year/month

    Parameters
    ----------
    line : list
        columnas de una línea de datos del fichero de entrada

    Returns
    -------
    fid0 : str
        id estación
    fecha0 : date
        fecha en line
    month0 : int
        mes en line
    d_values : list
        lista de nulos

    """
    ndays = (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)
    fid0 = line[0]
    fecha0 = datetime.strptime(line[1], "%Y-%m-%d")
    month0 = fecha0.month
    if month0 == 2:
        if isleap(fecha0.year):
            length = 29
        else:
            length = ndays[month0 - 1]
    else:
        length = ndays[month0 - 1]
    d_values = [NODATA] * length

    return (fid0, fecha0, month0, d_values)


def _write_row(d_values: [str], fid0: str, fecha0: datetime.date, 
               fo_writer: csv.writer):
    nulls = [item for item in d_values if item == NODATA]
    if len(nulls) != len(d_values):
        svalues = ','.join(d_values)
        svalues = '{' + svalues.replace(NODATA, 'null') + '}'
        row = [fid0, fecha0.year, fecha0.month, svalues]
        fo_writer.writerow(row)


def pdia_2_array_variable_len(sfi: str, sfo: str, header: bool = True, 
                              is_test:bool = True, nlines: int = 100) -> None:
    """
    A partir de un fichero de datos diarios (con nulos) del tipo id, 
    fecha, valor, escribe otro fichero con los datos diarios almacenados en un 
    array que puede ser importado en una DB Postgres y formato id, year, 
    month, array int2
    En el formato original cada dato diario es un registro (row); en el nuevo
    formato cada año/mes es un registro (row)
    El nuevo formato tiene interés cuando la estación tiene datos casi todos
    los días del mes, pues permite ahorrar mucho espacio en disco

    Parameters
    ----------
    sfi : str
        Fichero de entrada fmt csv: id, date, valor
    sfo : str
        Fichero de salida fmt csv: id, año, mes, array valores diarios
    header : bool, optional default True
        Si True la primera línea del fichero de datos es una cabecera 
    is_test: bool, optional default True
        la función se ejecuta en modo test, se lee un máximo de nlines del
        fichero de datos
    nlines: int, optional default 100
        número máximo de líneas del fichero de datos que se lee cuando 
        is_test es True
    Returns
    -------
    None

    """
    if header:
        first_data_line = 1
    else:
        first_data_line = 0
        
    with open(sfi, 'r', encoding='utf-8') as fi, \
    open(sfo, 'w', newline='', encoding='utf-8') as fo:
        fi_reader = csv.reader(fi, delimiter=',')
        fo_writer = csv.writer(fo, delimiter=',', quotechar='"', 
                               quoting=csv.QUOTE_MINIMAL)
        
        fo_writer.writerow(('fid', 'year', 'month', 'values'))
        for il, line in enumerate(fi_reader):
            if il < first_data_line:
                continue
            fecha = datetime.strptime(line[1], "%Y-%m-%d")
            if il == first_data_line:
                fid0, fecha0, month0, d_values = _init_v_variable_len(line)
            
            if line[0] != fid0 or fecha.month != month0:
                _write_row(d_values, fid0, fecha0, fo_writer)
                fid0, fecha0, month0, d_values = _init_v_variable_len(line)
                
            d_values[fecha.day - 1] = line[2]
            if is_test and il + 1 == nlines:
                print('Ejecución de prueba')
                break
        _write_row(d_values, fid0, fecha0, fo_writer)
    print(f'Se han grabado {il+1:d} datos')                    


def pdia_2_array_const_len(sfi: str, sfo: str, is_test:bool = True,
                           nlines: int = 100) -> None:
    """
    El formato del nuevo fichero es id, year,month, array de postgres de 31
    elements int2
    
    SI SE QUIERE UTILIZAR HAY QUE REESCRIBIRLA FIJÁNDOSE EN 
    pdia_2_array_variable_len

    Parameters
    ----------
    sfi : str
        Fichero de entrada fmt csv
    sfo : str
        Fichero de salida fmt csv

    Returns
    -------
    None

    """

    with open(sfi, 'r', encoding='utf-8') as fi, \
    open(sfo, 'w', newline='', encoding='utf-8') as fo:
        fi_reader = csv.reader(fi, delimiter=',')
        fo_writer = csv.writer(fo, delimiter=',', quotechar='"', 
                               quoting=csv.QUOTE_MINIMAL)
        
        fo_writer.writerow(('fid', 'year', 'month', 'values'))
        for il, line in enumerate(fi_reader):
            fecha = datetime.strptime(line[1], "%Y-%m-%d")
            if il == 0:
                fid0, fecha0, month0, d_values = _init_pdia(line, 'pdia3')
            if line[0] != fid0 or fecha.month != month0:
                svalues = ','.join(d_values)
                svalues = '{' + svalues.replace(NODATA, 'null') + '}'
                row = [fid0, fecha0.year, fecha0.month, svalues]
                fo_writer.writerow(row)
                fid0, fecha0, month0, d_values = _init_pdia(line, 'pdia3')
                
            d_values[fecha.day - 1] = line[2]
            if is_test and il + 1 == nlines:
                print('Ejecución de prueba')
                print(f'Se han grabado sólo los primeros {il+1:d} datos')
                return


def _init_pdia(line: list, func:str = 'pdia'):
    """
    
    Incialización de variables para pdia* functions

    Parameters
    ----------
    line : list
        contenidos de una línea del fichero de entrada

    Returns
    -------
    fid0 : str
        id estación
    fecha0 : date
        fecha en line
    month0 : int
        mes en line
    d_values : list
        lista de 31 nulos

    """
    fid0 = line[0]
    fecha0 = datetime.strptime(line[1], "%Y-%m-%d")
    month0 = fecha0.month
    if func == 'pdia3':
        d_values = [NODATA] * DAYS_IN_MONTH
    else:
        d_values = [''] * DAYS_IN_MONTH
    return (fid0, fecha0, month0, d_values)


def _get_header():
    """
    forma el header para pdia func

    Returns
    -------
    header : str
        header

    """
    days = [f'd{i+1:d}' for i in range(31)]
    header = ['fid', 'year', 'month'] + days
    return header


def pdia(sfi: str, sfo: str) -> None:
    """
    nuevo formar id, year,month,31 valores separados por ,

    Parameters
    ----------
    sfi : str
        Fichero de entrada fmt csv
    sfo : str
        Fichero de salida fmt csv

    Returns
    -------
    None
    """
    with open(sfi, 'r', encoding='utf-8') as fi, \
    open(sfo, 'w', newline='', encoding='utf-8') as fo:
        fi_reader = csv.reader(fi, delimiter=',')
        fo_writer = csv.writer(fo, delimiter=',', quotechar='"', 
                               quoting=csv.QUOTE_MINIMAL)
        
        fo_writer.writerow(_get_header())
        for il, line in enumerate(fi_reader):
            fecha = datetime.strptime(line[1], "%Y-%m-%d")
            if il == 0:
                fid0, fecha0, month0, d_values = _init_pdia(line)
            if line[0] != fid0 or fecha.month != month0:
                row = [fid0, fecha0.year, fecha0.month] + d_values
                fo_writer.writerow(row)
                fid0, fecha0, month0, d_values = _init_pdia(line)
                
            d_values[fecha.day - 1] = line[2]


def pdia_create_table(sfo: str, table_name: str) -> None:
    """
    create table command for data created in pdia

    Parameters
    ----------
    sfo : str
        Fichero sql de salida
    table_name : str
        nombre de la tabla

    Returns
    -------
    None
    """

    a = f'create table if not exists {table_name} (\nfid varchar(6),\n' +\
        'year int2,\nmonth int2,\n'
    b = ',\n'.join([f'd{i+1:d} int2' for i in range(DAYS_IN_MONTH)])
    c = ',\nprimary key (fid, year, month)\n);'    
    with open(sfo, 'w', encoding='utf-8') as fo:
        for item in (a, b, c):
            fo.write(item)                


def pdia2(sfi: str, sfo: str, is_test:bool = True, nlines: int = 100) -> None:
    """
    nuevo formar id, year,month,string con 31 valores separados por ,

    Parameters
    ----------
    sfi : str
        Fichero de entrada fmt csv
    sfo : str
        Fichero de salida fmt csv

    Returns
    -------
    None

    """

    with open(sfi, 'r', encoding='utf-8') as fi, \
    open(sfo, 'w', newline='', encoding='utf-8') as fo:
        fi_reader = csv.reader(fi, delimiter=',')
        fo_writer = csv.writer(fo, delimiter=',', quotechar='"', 
                               quoting=csv.QUOTE_MINIMAL)
        
        fo_writer.writerow(('fid', 'year', 'month', 'values'))
        for il, line in enumerate(fi_reader):
            fecha = datetime.strptime(line[1], "%Y-%m-%d")
            if il == 0:
                fid0, fecha0, month0, d_values = _init_pdia(line)
            if line[0] != fid0 or fecha.month != month0:
                svalues = ','.join(d_values)
                row = [fid0, fecha0.year, fecha0.month, svalues]
                fo_writer.writerow(row)
                fid0, fecha0, month0, d_values = _init_pdia(line)
                
            d_values[fecha.day - 1] = line[2]
            if is_test and il + 1 == nlines:
                print('Ejecución de prueba')
                print(f'Se han grabado sólo los primeros {il+1:d} datos')
                return
