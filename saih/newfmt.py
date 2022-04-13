# -*- coding: utf-8 -*-
"""
Created on Tue Apr 12 13:38:53 2022

@author: solis
"""
import csv
import glob
from os.path import basename, isfile


def files(org, ext='csv'):
    """
    Files in directory with extension ext

    Parameters
    ----------
    org : str
        directory
    ext : str
        extension. The default is 'csv'.

    Returns
    -------
    list[str]
        file names

    """

    if ext == 'csv':
        return glob.glob(org + f"\*.{ext}")
    else:
        return []


def write_newfmt(files, header, dst, sep=','):
    """
    writes saih csv files in a new format

    Parameters
    ----------
    files : list[str]
        list of paths do data files in saih fmt
    header: list[str]
        column names
    dst : str
        csv output file
    sep : str
        column separator in files

    Returns
    -------
    None.
    """
    def id_get(row):
        """
        Read the station identifier in the first row of the csv file

        Parameters
        ----------
        row : list[str]
            First row of the file

        Returns
        -------
        saih station identifier

        """
        return row[1][0:5]


    with open(dst, mode='w', newline='') as fo:
        writer = csv.writer(fo, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(header)
        for ifname, fname in enumerate(files):
            with open(fname) as fi:
                print(basename(fname))
                reader = csv.reader(fi, delimiter=sep)
                for nrow, row in enumerate(reader):
                    if nrow == 0:
                        id = id_get(row)
                    else:
                        row[0] = row[0][0:10]
                        writer.writerow([id,] + row)


def events(org, dst, delimiter=','):
    """
    Readss pp in org and writes only events pp>0 limited by 0 in the the time
    before and after it

    Parameters
    ----------
    org : str
        csv input file
    dst : text
        csv output file

    Returns
    -------
    None.

    """
    def pp_get(row):
        return float(row[2])

    def dif_time_get(datet2, datet1, step='day', sep='-'):
        """
        Calculates the difference in step unit between datet2 and datet1

        Parameters
        ----------
        row : list[str]
            current row date with fmt yyyy-mm-dd
        row_end_event : list[str]
            row last event
        step : str
            date or timestamp difference between consecutive rows
        sep : str
            day, mont, year separator

        Returns
        -------
        None.

        """



    if isfile(dst):
        ask = input('The output file already exists, continue? y/n: ')
        if ask.lower() != 'y':
            return

    with open(org) as fi, open(dst, mode='w', newline='') as fo:
        reader = csv.reader(fi, delimiter=",")
        writer = csv.writer(fo, delimiter=delimiter, quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for nrow, row in enumerate(reader):
            print(nrow)
            if nrow == 0:
                writer.writerow(row)
            elif nrow == 1:
                writer.writerow(row)
                prev_row = list(row)
                xpp = pp_get(row)
                if xpp > 0.:
                    in_event = True
                else:
                    in_event = False
                    zero_end = row[1]
            else:
                xpp = pp_get(row)
                if in_event == True:
                    writer.writerow(row)
                    if xpp <= 0.:
                        in_event = False
                        zero_end = row[1]
                else:
                    if xpp > 0.:
                        if in_event == False:
                            in_event = True
                            if zero_end != prev_row[1]:
                                writer.writerow(prev_row)
                        writer.writerow(row)
                    else:
                        if in_event == True:
                            in_event = False
                            writer.writerow(row)
                prev_row = list(row)

        if in_event == False:
            writer.writerow(row)


