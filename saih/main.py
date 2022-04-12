# -*- coding: utf-8 -*-
"""
Created on Sun Apr 10 12:15:01 2022

@author: solis
"""
import littleLogging as logging

# ============Change saih format===========================
org = r'H:\LSGB\20220324_informe_pz\data_chs\saih'
dst = r'H:\LSGB\20220324_informe_pz\data_chs\saih\newfmt\data.csv'
header = ("id","fecha","ppmm")

# ============Write events only============================
org = r'H:\LSGB\20220324_informe_pz\data_chs\saih\newfmt\data.csv'
dst = r'H:\LSGB\20220324_informe_pz\data_chs\saih\newfmt\data_events.csv'

write_events = True

if __name__ == "__main__":

    try:
        from time import time
        import traceback

        import newfmt as nf

        startTime = time()

        files = nf.files(org)
        print('Files in org')
        for f in files:
            print(f)
        ask = input('Continue? y/n: ')
        if ask.lower() == 'y':
            files = nf.write_newfmt(files, header, dst)

        if write_events:
            nf.events(org, dst)

        xtime = time() - startTime
        print(f'El script tardó {xtime:0.1f} s')

    except ValueError:
        msg = traceback.format_exc()
        logging.append(f'ValueError exception\n{msg}')
    except ImportError:
        msg = traceback.format_exc()
        print (f'ImportError exception\n{msg}')
    except Exception:
        msg = traceback.format_exc()
        logging.append(f'Exception\n{msg}')
    finally:
        logging.dump()
        print('\nFin')
