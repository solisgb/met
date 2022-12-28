# -*- coding: latin-1 -*-

"""
parametros iniciales del script
"""

"""
posiciones de las columnas que se van a pasar a un nuevo formato y que
pueden variar según el fichero que facilita AEMET
¡OJO! poner el número de columna-1
__________________________________________________________________
columna códigos de la estación - 1 (si es la primera poner 0"""
ID = 0
"""columna año datos"""
YEAR = 1
"""columna mes datos"""
MONTH = 2
"""columna nombre de la estación"""
NAME = 3
"""columna primer dato del mes de P diaria"""
P1 = 4
"""columna primer dato del mes de TMAX diaria"""
TMAX = 35
"""columna primer dato del mes de TIN diaria"""
TMIN = 66

"""NOMBRE DE FICHEROS Y DIRECTORIOS
_____________________________________________________________________
directorio del fichero de datos de AEMET"""
# DIR_DAT = r'C:\Users\solil\Documents\_D\aemet_pt_2017'
DIR_DAT = r'\\intsrv1008\SGD\00_Proyectos\42143\100_TRABAJO\100_10_DOC_COMUN\aemet2018nov'

"""directorio de los ficheros de resultados"""
# DIR_OUT = r'C:\Users\solil\Documents\_D\aemet_pt_2017\out'
DIR_OUT = r'\\intsrv1008\SGD\00_Proyectos\42143\100_TRABAJO\100_10_DOC_COMUN\aemet2018nov\out'

"""Nombre del fichero de texto único de AEMET donde se encuentran los datos
   de precipipitación, temperatura máxima y mínima diaria"""
AEMETPT = '300180302_test.txt'

"""Nombre del fichero de resultados con las estaciones meteorológicas"""
FESTACIONES = 'estaciones.txt'

"""Nombre del fichero de resultados con la precipitación diaria"""
FP = 'p.txt'

"""Nombre del fichero de resultados con la temperatura máxima diaria"""
FTMAX = 'tmax.txt'

"""Nombre del fichero de resultados con la temperatura mínima diaria"""
FTMIN = 'tmin.txt'
