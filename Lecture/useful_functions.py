# -*- coding: utf-8 -*-
"""
Created on Thu Mar 23 07:49:59 2023

@author: jrbrad
"""

from numpy import linalg
import numpy as np

def cos_sim(vec1, vec2):
    vec1,vec2 = np.array(vec1), np.array(vec2)
    return vec1@vec2/(linalg.norm(vec1) * linalg.norm(vec2))

if __name__ == '__main__':
    print(dist((0,0), (3,4)))
    print(cos_sim((1,1),(1,1)))
    print(cos_sim((1,1),(-1,-1)))
    print(cos_sim((1,1),(0,1)))
