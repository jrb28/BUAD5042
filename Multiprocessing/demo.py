# -*- coding: utf-8 -*-
"""
Created on Fri Apr 14 10:39:01 2023

@author: jrbrad
"""

import numpy as np
import math

def dist_loops_py(p,q):
    dist = []
    for i in range(p.shape[0]):
        new_row = []
        for j in range(q.shape[0]):
            this_sum = 0.
            for k in range(p.shape[1]):
                this_sum += (p[i][k] -q[j][k])**2
            new_row.append(math.sqrt(this_sum))
        dist.append(new_row)

    return dist


def dist_loops(p,q):
    dist = np.zeros((p.shape[0],q.shape[0]))
    for i in range(p.shape[0]):
        for j in range(q.shape[0]):
            dist[i][j] = np.sqrt(sum((p[i] -q[j])**2))
    return dist


def dist_la(p,q):
    pp = (p*p).sum(axis=1)
    qq = (q*q).sum(axis=1)
    pq = np.dot(p,q.T)
    return np.sqrt(pp[:,np.newaxis] - 2*pq + qq)




