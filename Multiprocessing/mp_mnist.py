# -*- coding: utf-8 -*-
"""
Created on Tue Feb 20 14:11:57 2024

@author: jrbrad
"""

import numpy as np
import time
import multiprocessing as mp

def dist_mnist(size):
    p = np.load(f'data/mnist1_{size}.npy').astype(np.float32)
    q = np.load(f'data/mnist2_{size}.npy').astype(np.float32)
    assert p.shape[0] == q.shape[0]
    assert p.shape[1] == 784
    assert q.shape[1] == 784
    n = p.shape[0]

    result = np.zeros((n,n)).astype(np.float32)
    for i in range(n):
        for j in range(n):
            result[i][j] = np.sqrt(q[i]@q[i]-2*p[j]@q[i]+p[j]@p[j])
    print(f'Done with {size}')
    return result
    
if __name__ == '__main__':    
    sizes = [1000, 100, 1000, 100, 10, 1000, 10] # [100 for _ in range(5)] 
    
    ''' Sequential processing '''
    start = time.time()
    result = []
    for size in sizes:
        result.append(dist_mnist(size))
    print(f'Exec. time for sequential execution: {time.time() - start}')
    
    ''' Multiprocessing '''
    start = time.time()
    with mp.Pool(5) as pool:
      result = pool.map(dist_mnist, sizes)
    print(f'Exec. time for paallel execution: {time.time() - start}')
    