# -*- coding: utf-8 -*-
"""
Created on Thu Apr 06 11:56:04 2017

@author: jrbrad
"""

import requests
import time
import multiprocessing
from lxml import objectify

""" http://w1.weather.gov/xml/current_obs/seek.php?state=va&Find=Find """

def getWeather(ext):  
    URL = 'http://w1.weather.gov/xml/current_obs/'
    fields = ['location','station_id','latitude','longitude','temp_f','weather','wind_dir','wind_degrees','wind_mph','wind_gust_mph','pressure_in','visibility_mi','wind_string']
    response = requests.get(URL+ext).content
    root = objectify.fromstring(response)
    """ Build response """
    blank = {}
    for tag in fields:
        try:
            if isinstance(root[tag],float):
                blank[tag] = root[tag]
            else:
                blank[tag] = str(root[tag]) 
        except:
            continue
    return blank

if __name__ == "__main__":
    exts = ['KVJI.xml', 'KOFP.xml', 'K0V4.xml', 'KCHO.xml', 'KCXE.xml', 'KCPK.xml', 'KFCI.xml', 'KW63.xml', 'KW81.xml', 'KCJR.xml', 'KDAN.xml', 'KPSK.xml', 'KW13.xml', 'KEMV.xml', 'KFVX.xml', 'KNFE.xml', 'KDAA.xml', 'KFAF.xml', 'KFKN.xml', 'KEZF.xml', 'KFRR.xml', 'KBKT.xml', 'KGVE.xml', 'KHLX.xml', 'KHSP.xml', 'K7W4.xml', 'KLFI.xml', 'KLVL.xml', 'K0VG.xml', 'KJYO.xml', 'KLKU.xml', 'KW31.xml', 'KLUA.xml', 'KLYH.xml', 'KHEF.xml', 'KMKJ.xml', 'KMTV.xml', 'KMFV.xml', 'KW96.xml', 'K8W2.xml', 'KPHF.xml', 'KPVG.xml', 'KNGU.xml', 'KORF.xml', 'KOMH.xml', 'KPTB.xml', 'KNYG.xml', 'KRIC.xml', 'KROA.xml', 'KW75.xml', 'KAVC.xml', 'KRMN.xml', 'KSHD.xml', 'KSFQ.xml', 'KXSA.xml', 'KJFZ.xml', 'KNTU.xml', 'KBCB.xml', 'KAKQ.xml', 'KWAL.xml', 'KHWY.xml', 'KIAD.xml', 'KDCA.xml', 'KFYJ.xml', 'KW78.xml', 'KJGG.xml', 'KOKV.xml', 'KLNP.xml']
    print('NOAA XML Data')
    
    ''' Serial execution '''
    start = time.time()
    for ext in exts:
        result = getWeather(ext)
        print(ext + ":", result)
        
    exec_time_serial = time.time() - start
    
    ''' Multiprocessing '''
    pool = multiprocessing.Pool(10)         # create process pool using multiple CPUs
    start = time.time()
    results = pool.map(getWeather,exts)  # creates a separate process for each value in values list
    #results = pool.imap_unordered(getWeather,exts)  # creates a separate process for each value in values list
    pool.close()         # done creating processes in pool
    pool.join()          # wait until all processes are complete before continuing
    for x in results:
        print('\t', x)
    print(f'Execution time (parallel): {time.time() - start} seconds')
    print("Execution time (serial):",exec_time_serial)