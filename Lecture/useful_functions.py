# -*- coding: utf-8 -*-
"""
Created on Thu Mar 23 07:49:59 2023

@author: jrbrad
"""

def cos_sim(vec1, vec2):
    d_prod = sum(vec1[i]*vec2[i] for i in range(len(vec1)))
    return d_prod/(dist((0,0), vec1) * dist((0,0), vec2))

def dist(loc1, loc2):
    return ((loc1[0] - loc2[0])**2 + (loc1[1] - loc2[1])**2)**0.5

if __name__ == '__main__':
    print(dist((0,0), (3,4)))
    print(cos_sim((1,1),(1,1)))
    print(cos_sim((1,1),(-1,-1)))
    print(cos_sim((1,1),(0,1)))
