# -*- coding: utf-8 -*-
"""
Created on Wed Jan  3 08:56:03 2024

@author: jrbrad
"""

import numpy as np

def read_data(fname_A, fname_c):
    A = np.loadtxt(fname_A)
    b = 30
    c = np.loadtxt(fname_c)
    return A,b,c
    
def init(n, m, perc):
    ''' More intuitive approach '''
    pop = np.zeros((n,m))
    pop[np.random.random(size=(n,m))<=perc] = 1
    ''' Alternate (faster) approach '''
    #pop = np.random.choice(np.array([0,1]), size=(n,m), p=(1-perc,perc))
    return pop

def feasible(pop,c,budget):
    for i in range(pop.shape[0]):
        ''' randomly delete locations until within budget '''
        while pop[i]@c > budget:
            ''' Randomly choose a "selected" location '''
            idx = np.random.choice(np.arange(pop.shape[1])*(pop[i]==1))
            pop[i,idx] = 0

def fitness(pop,A):
    return ((pop@A)>0).sum(axis=1)

def select(pop, fit):
    ''' Compute probability distribution for choosing parents '''
    prob = fit/sum(fit)
    parents = np.random.choice(np.arange(pop.shape[0]), size=(pop.shape[0],2), p = prob)
    return parents

def crossover(parents,pop):
    crosspts = np.random.randint(0,pop.shape[1],size=pop.shape[0])
    #idx = np.tile(np.arange(pop.shape[1]), pop.shape[0]).reshape(pop.shape[0],pop.shape[1])
    idx = np.tile(np.arange(pop.shape[1]), (pop.shape[0],1))
    par_left_mask = np.ones(pop.shape)*(idx<=crosspts.reshape(pop.shape[0],1))
    par_right_mask = np.ones(pop.shape)*(idx>crosspts.reshape(pop.shape[0],1))
    pop = pop[parents[:,0]]*par_left_mask + pop[parents[:,1]]*par_right_mask

def mutate(pop, perc):
    mut_idx = np.random.random(pop.shape)<=perc
    pop[mut_idx] = 1 - pop[mut_idx]

def stat(pop, fit, best_fit, best_soln):
    if fit.max() > best_fit:
        return fit.max(), pop[fit.argmax()].copy()
    else:
        return best_fit, best_soln
    
    

def report(i, best_fit, fit):
    print(f'Generation {i}: Best fit: {best_fit}; Max fit gen:{fit.max()}; Avg fit gen: {fit.mean()}')
    
''' Input data '''
A,budget,c = read_data('A.txt', 'c.txt')
num_loc = A.shape[0]
num_dest = A.shape[1]

''' GA parameters '''
n = 20 # population size
num_gen = 200
init_perc = 0.05 # expected percentage of possible locations 
                 # selected in initial candidate solutions
mutate_perc = 0.001

''' Initialize population '''
pop = init(n, num_loc, init_perc)
feasible(pop,c,budget) # note that function modifies population directly
fit = fitness(pop,A)
best_fit, best_soln = stat(pop, fit, 0, np.zeros(num_loc))

''' Evolution '''
for i in range(num_gen):
    report(i, best_fit, fit)
    parents = select(pop, fit)
    crossover(parents,pop) # replace population with offspring
    mutate(pop, mutate_perc)
    feasible(pop,c,budget)
    fit = fitness(pop,A)
    best_fit, best_soln = stat(pop, fit, best_fit, best_soln)
    