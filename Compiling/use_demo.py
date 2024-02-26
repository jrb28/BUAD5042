# -*- coding: utf-8 -*-
"""
Created on Fri Apr 14 10:42:38 2023

@author: jrbrad
"""

''' Import compiled code file '''
import demo

import numpy as np
import time
import math

nlocs1, nlocs2 = 1000, 1000
p = np.random.randint(0,12,size=(nlocs1,2))
q = np.random.randint(0,12,size=(nlocs2,2))


''' Python Loops '''
time_start = time.time()
dist = []
for i in range(p.shape[0]):
    new_row = []
    for j in range(q.shape[0]):
        this_sum = 0.
        for k in range(p.shape[1]):
            this_sum += (p[i][k] - q[j][k])**2
        new_row.append(math.sqrt(this_sum))
    dist.append(new_row)
print(f'Execution time for {nlocs1} by {nlocs2} location pairs with Python loops: {time.time()-time_start} seconds')



time_start = time.time()
dist = demo.dist_loops_py(p,q)
print(f'Execution time for {nlocs1} by {nlocs2} location pairs with compiled Python loops: {time.time()-time_start} seconds')



''' Python loop solution with numpy '''
time_start = time.time()
dist = np.zeros((p.shape[0],q.shape[0]))
for i in range(p.shape[0]):
    for j in range(q.shape[0]):
        dist[i][j] = np.sqrt(sum((p[i] -q[j])**2))
print(f'\n\n\nExecution time for {nlocs1} by {nlocs2} location pairs with Python/numpy loops: {time.time()-time_start} seconds')
print(f'Distance array shape: {dist.shape}')


time_start = time.time()
dist = demo.dist_loops(p,q)
print(f'Execution time for {nlocs1} by {nlocs2} location pairs with compiled Python/numpy loops: {time.time()-time_start} seconds')
print(f'Distance array shape: {dist.shape}')



''' Using linear algebra transformation '''
time_start = time.time()
pp = (p*p).sum(axis=1)
qq = (q*q).sum(axis=1)
pq = np.dot(p,q.T)
result =  np.sqrt(pp[:,np.newaxis] - 2*pq + qq)
print(f'\n\n\nExecution time for LA soln: {time.time() - time_start} seconds; Result dimension: {dist.shape}')

time_start = time.time()
dist = demo.dist_la(p,q)
print(f'Execution time for compiled LA soln: {time.time() - time_start} seconds; Result dimension: {dist.shape}')

