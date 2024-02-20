# -*- coding: utf-8 -*-
"""
Created on Thu Mar 30 13:44:11 2017

@author: jrbrad
"""

def factorial(num):
    if num ==1:
        return 1
    else:
        return num * factorial(num-1)
        
if __name__ == "__main__":
    print(factorial(4))