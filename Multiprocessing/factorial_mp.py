# -*- coding: utf-8 -*-
"""
Created on Thu Apr 06 09:39:58 2017

@author: jrbrad
"""

import multiprocessing as mp
import time

def factorial(num):
    if num ==1:
        return 1
    else:
        return num * factorial(num-1)
        
if __name__ == '__main__':
    values = range(50,100)
    pool = mp.Pool(5)         # uses 5 CPU cores for mp
    time_start = time.time()
    # execute call_fact in a separate process for each element in values 
    results = pool.map(factorial,values)  
    pool.close()         # done creating processes in pool
    pool.join()          # wait until all processes are complete before continuing
    print([x for x in results])
    print(f'Execution time w/multiprocessing: {time.time() - time_start} seconds\n\n')
    
    time_start = time.time()
    result = []
    for val in values:
        result.append(factorial(val))
    print(result)
    print(f'Sequential execution time on 1 CPU: {time.time() - time_start} seconds')