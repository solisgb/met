# -*- coding: utf-8 -*-
"""
Created on Wed Dec 21 14:06:52 2022

@author: solis
"""

try:
    from time import time
    import traceback
    
    import meteoro_new_format as met
    import littleLogging as logging
except ImportError as e:
    print( getattr(e, 'message', repr(e)))
    raise SystemExit(0)
    

if __name__ == "__main__":

    startTime = time()

    try:
         
        fdata = r'E:\DB\bda\cli\p.csv'
        fout = r'E:\DB\bda\cli\p_dia_nuevo_formato4.csv'        
        met.pdia_2_array_variable_len(fdata, fout, header = False, 
                                      is_test=False)        

    except ValueError:
        msg = traceback.format_exc()
        logging.append(msg)
    except Exception:
        msg = traceback.format_exc()
        logging.append(msg)
    finally:
        logging.dump()
        xtime = time() - startTime
        print(f'El script tardó {xtime:0.1f} s')


