# -*- coding: latin-1 -*-

"""
parametros iniciales del script
"""

"""
posiciones de las columnas que se van a pasar a un nuevo formato y que
pueden variar seg�n el fichero que facilita AEMET
�OJO! poner el n�mero de columna-1
__________________________________________________________________
columna c�digos de la estaci�n - 1 (si es la primera poner 0"""
ID = 0
"""columna a�o datos"""
YEAR = 1
"""columna mes datos"""
MONTH = 2
"""columna nombre de la estaci�n"""
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

"""Nombre del fichero de texto �nico de AEMET donde se encuentran los datos
   de precipipitaci�n, temperatura m�xima y m�nima diaria"""
AEMETPT = '300180302_test.txt'

"""Nombre del fichero de resultados con las estaciones meteorol�gicas"""
FESTACIONES = 'estaciones.txt'

"""Nombre del fichero de resultados con la precipitaci�n diaria"""
FP = 'p.txt'

"""Nombre del fichero de resultados con la temperatura m�xima diaria"""
FTMAX = 'tmax.txt'

"""Nombre del fichero de resultados con la temperatura m�nima diaria"""
FTMIN = 'tmin.txt'
