# -*- coding: latin-1 -*-

"""
lee el fichero de P, Tmax y Tmin diaria de un único fichero de AEMET que
    contiene todos tipos de datos1
Los contenidos de los ficheros de datos no están estandarizados en cuanto al
    número de datos que se dan de las estaciones propiamente dichas. En unos
    casos dan indicativo, año, mes, nombre, coordenadas... y en otros casos
    dan menos.
Por lo tanto, antes de ejecutar el programa hay que abrir el fichero de datos
    facilitado y ver en que posiciones -empezando por 0 para la primera
    posición -columna- se sitúan el primer dato de p, el primero de tmax y el
    primero de tmin
Más explicaciones en import_AEMET
Datos s suministrar por el usuario en import_AEMET_parameters
"""

if __name__ == "__main__":

    try:
        from datetime import timedelta
        from time import time
        from comunes import query_yes_no
        import import_AEMET as aemet

        aemet.print_parameters()
        a = query_yes_no('¿Desea continuar?')

        if a:

            startTime = time()
            print('Procesando')
            aemet.change_format_diary_data()

        else:
            print('script interrumpido por el usuario')

        xtime = time() - startTime
        print('The script took {0}'.format(str(timedelta(seconds=xtime))))
    except Exception as e:
        import traceback
        import logging
        logging.error(traceback.format_exc())
    finally:
        print('fin')
