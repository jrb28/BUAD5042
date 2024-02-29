# -*- coding: utf-8 -*-
"""
Created on Wed Feb 28 08:57:24 2024

@author: jrbrad
"""

import numpy as np
import time
import multiprocessing as mp

def chunk(idx_beg, idx_end):
    size = 60000
    p = np.load(f'data/mnist1_{size}.npy').astype(np.float32)
    q = np.load(f'data/mnist2_{size}.npy').astype(np.float32)[idx_beg:idx_end]
    
    return np.einsum('ij,jk->ik',-2*q,p.T)

if __name__ == '__main__':    
    chunks = 30
    size = 60000
    chunksize = int(size/chunks)
    idx = [(i*chunksize, (i+1)*chunksize) for i in range(chunks)] 
    start = time.time()
    
    pool = mp.Pool(5)
    result = pool.starmap(chunk, idx)
    pool.close()
    pool.join()
    result = np.vstack(result)
    
    ''' Square images in q and delete data'''
    q = np.load(f'data/mnist2_{size}.npy').astype(np.float32)
    n = q.shape[0]
    result += np.einsum('ij,ij->i',q,q)[:,np.newaxis]
    del q
    
    ''' Square images in p and delete data'''
    p = np.load(f'data/mnist1_{size}.npy').astype(np.float32)
    result += np.einsum('ij,ij->i',p,p) 
    del p
    
    ''' Take square root '''
    result = np.sqrt(result)
    
    ''' Print results '''
    print(f'Exec. time: {time.time() - start} for {n}x{n}' )
    print(result[0,:5])