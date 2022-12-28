# -*- coding: latin-1 -*-

"""
lectura y escritura de P, TMAX y TMIN de AEMET en nuevo formato
    se graban hasta 4 ficheros; estaciones con datos, datos P, TMAX y TMIN
los datos del fichero de AEMET de datos diarios de P, TMAX y TMIN son
    facilitados en distintos formatos, que dependen generalmente de los
    datos de características de las estaciones que suministran
Dependiendo de los datos suministrados cambian las posiciones de los
    datos de P, TMX y TMIN, que se suministran en el módulo
    import_AEMET_parameters
Los datos básicos de características de las estaciones que se consideran son
    su código y el nombre, que se controlan a través de los valores de
    ID y NAME en import_AEMET_parameters. Si en un fichero de AEMET no viene
    el nombre de la estación, hay que modificar las funciones
    write_stations_head, write_stations_features y change_format_diary_data
    -esta última es en la que se hacen las llamadas
    Lo mismo pasaría si vienen más características de las extaciones y se
    quieren escribir en el fichero de estaciones datos adicionales -por
    ejemplo las coordenadas-
"""

BUFSIZE_WESTACIONES = 10240
BUFSIZE_WRESTO = 102400
SUFFIX_FILE_NODAT = '_void'


def print_parameters():
    import import_AEMET_parameters as par
    """imprime los parámetros del script"""
    print('dir datos: {}'.format(par.DIR_DAT))
    print('Fichero en formato AEMET: {}'.format(par.AEMETPT))
    print('ficheros de salida nuevo formato')
    print('dir resultados: {}'.format(par.DIR_OUT))
    print('Estaciones: {}'.format(par.FESTACIONES))
    print('P dmm {}'.format(par.FP))
    print('Tmax dgradoC {}'.format(par.FTMAX))
    print('Tmin dgradoC {}'.format(par.FTMIN))


def get_name(name):
    """añade el sufijo SUFFIX_FILE_NODAT al nombre de un fichero"""
    from os.path import splitext
    a = splitext(name)
    return a[0] + SUFFIX_FILE_NODAT + a[1]


def write_stations_head(fw):
    """
    La cabecera puede cambiar segun el fichero de datos que facilita AEMET
    """
    fw.write('INDICATIVO\tNOMBRE\n')


def write_stations_features(fw, words):
    """
    Los datos de las estaciones pueden cambiar
     segun el fichero de datos que facilita AEMET
    """
    import import_AEMET_parameters as par
    fw.write('{0}\t{1}\n'.format(words[par.ID], words[par.NAME]))


def write_station_values(nd, d0, ip, fw, fwv, words, D1):
    """
    escribe los valores de código de estación, fecha y variable meteorológica
    (P, TMAX o TMIN)
    """
    import import_AEMET_parameters as par
    for i in range(nd):
        if len(words[ip]) > 0:
            if int(words[ip]) < 0:
                words[ip] = '0'
            fw.write('{0}\t{1}\t{2}\n'.format(words[par.ID],
                     d0.strftime('%d/%m/%Y'), words[ip]))
        else:
            fwv.write('{0}\t{1}\n'.format(words[par.ID],
                      d0.strftime('%d/%m/%Y')))
        d0 = d0 + D1
        ip += 1


def change_format_diary_data():
    """
    FORMATO AEMET NOV. 2018
    lee el fichero suministrado por AEMET y escribe varios ficheros en el
        formato deseado:
            Un fichero de estaciones en el fichero de AEMET
            Un fichero para cada variable Pdiaria, Tmax diaria, Tmin diaria
            Un fichero con sufijo SUFFIX_FILE_NODAT para cada variable que
                indica los datos que faltan
    """
    from calendar import monthrange
    from datetime import date, timedelta
    from os.path import join
    import import_AEMET_parameters as par

    fstations = open(join(par.DIR_OUT, par.FESTACIONES),
                     'w', BUFSIZE_WESTACIONES)

    fp = open(join(par.DIR_OUT, par.FP), 'w', BUFSIZE_WRESTO)
    name = get_name(par.FP)
    fp_void = open(join(par.DIR_OUT, name), 'w', BUFSIZE_WRESTO)

    ftmax = open(join(par.DIR_OUT, par.FTMAX), 'w', BUFSIZE_WRESTO)
    name = get_name(par.FTMAX)
    ftmax_void = open(join(par.DIR_OUT, name), 'w', BUFSIZE_WRESTO)

    ftmin = open(join(par.DIR_OUT, par.FTMIN), 'w', BUFSIZE_WRESTO)
    name = get_name(par.FTMIN)
    ftmin_void = open(join(par.DIR_OUT, name), 'w', BUFSIZE_WRESTO)

    stations = []

    lines = [line.rstrip('\n') for line in open(join(par.DIR_DAT,
             par.AEMETPT), 'r')]

    write_stations_head(fstations)

    for line in lines[1:]:
        words = line.split(';')

        if words[par.ID] not in stations:
            print(words[par.ID])
            stations.append(words[par.ID])
            write_stations_features(fstations, words)

        nd = monthrange(int(words[par.YEAR]), int(words[par.MONTH]))[1]
        d0 = date(int(words[par.YEAR]), int(words[par.MONTH]), 1)
        D1 = timedelta(days=1)

        # P
        ip = par.P1
        write_station_values(nd, d0, ip, fp, fp_void, words, D1)

        # TMAX
        ip = par.TMAX
        write_station_values(nd, d0, ip, ftmax, ftmax_void, words, D1)

        # TMIN
        ip = par.TMIN
        write_station_values(nd, d0, ip, ftmin, ftmin_void, words, D1)

    files = (fstations, fp, fp_void, ftmax, ftmax_void, ftmin, ftmin_void)
    for file in files:
        file.flush()
        file.close()


def change_format():
    """
    Esta fue la primera función que se escribio para pasar los datos
        de AEMET pedidos en 2017
    No lee las posiciones de import_AEMET_parameters
    lee el fichero suministrado por AEMET y escribe varios ficheros en el
        formato deseado:
            Un fichero de estaciones en el fichero de AEMET
            Un fichero para cada variable Pdiaria, Tmax diaria, Tmin diaria
            Un fichero con sufijo SUFFIX_FILE_NODAT para cada variable que
                indica los datos que faltan
    """
    from calendar import monthrange
    from datetime import date, timedelta
    from os.path import join
    import import_AEMET_parameters as par

    festaciones = open(join(par.DIR_OUT, par.FESTACIONES),
                       'w', BUFSIZE_WESTACIONES)
    festaciones.write('INDICATIVO\tNOMBRE\tALTITUD\tC_X\tC_Y\tNOM_PROV\t' +
                      'LONGITUD\tLATITUD\n')

    fp = open(join(par.DIR_OUT, par.FP), 'w', BUFSIZE_WRESTO)
    name = get_name(par.FP)
    fp_void = open(join(par.DIR_OUT, name), 'w', BUFSIZE_WRESTO)

    ftmax = open(join(par.DIR_OUT, par.FTMAX), 'w', BUFSIZE_WRESTO)
    name = get_name(par.FTMAX)
    ftmax_void = open(join(par.DIR_OUT, name), 'w', BUFSIZE_WRESTO)

    ftmin = open(join(par.DIR_OUT, par.FTMIN), 'w', BUFSIZE_WRESTO)
    name = get_name(par.FTMIN)
    ftmin_void = open(join(par.DIR_OUT, name), 'w', BUFSIZE_WRESTO)

    D1 = timedelta(days=1)
    estaciones = []

    lines = [line.rstrip('\n') for line in open(join(par.DIR_DAT,
             par.AEMETPT), 'r')]
    for line in lines[1:]:
        words = line.split(';')

        if words[0] not in estaciones:
            print(words[0])
            estaciones.append(words[0])
            festaciones.write('{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t{7}\n'
                              .format(words[0], words[3], words[4],
                                      words[5], words[6], words[7],
                                      words[8], words[9]))
        nd = monthrange(int(words[1]), int(words[2]))[1]
        d0 = date(int(words[1]), int(words[2]), 1)
        ip = 10

        # P
        for i in range(nd):
            if len(words[ip]) > 0:
                if int(words[ip]) < 0:
                    words[ip] = '0'
                fp.write('{0}\t{1}\t{2}\n'.format(words[0],
                         d0.strftime('%d/%m/%Y'), words[ip]))
            else:
                fp_void.write('{0}\t{1}\n'.format(words[0],
                              d0.strftime('%d/%m/%Y')))
            d0 = d0 + D1
            ip += 1

        # TMAX
        itmax = 41
        d0 = date(int(words[1]), int(words[2]), 1)
        for i in range(nd):
            if len(words[itmax]) > 0:
                ftmax.write('{0}\t{1}\t{2}\n'.format(words[0],
                            d0.strftime('%d/%m/%Y'), words[itmax]))
            else:
                ftmax_void.write('{0}\t{1}\n'.format(words[0],
                                 d0.strftime('%d/%m/%Y')))
            d0 = d0 + D1
            itmax += 1

        # TMIN
        itmin = 72
        d0 = date(int(words[1]), int(words[2]), 1)
        for i in range(nd):
            if len(words[itmin]) > 0:
                ftmin.write('{0}\t{1}\t{2}\n'.format(words[0],
                            d0.strftime('%d/%m/%Y'), words[itmin]))
            else:
                ftmin_void.write('{0}\t{1}\n'.format(words[0],
                                 d0.strftime('%d/%m/%Y')))
            d0 = d0 + D1
            itmin += 1

    files = [festaciones, fp, fp_void, ftmax, ftmax_void, ftmin, ftmin_void]
    for file in files:
        file.flush()
        file.close()
