# -*- coding: utf-8 -*-
"""
Created on Fri Sep 29 11:38:18 2023

@author: jrbrad
"""

import numpy as np
import time

def pop_gen(pop_size, num_tasks, num_workers):
    idx = np.random.randint(0, num_workers, size=(num_tasks*pop_size,))
    pop = np.zeros((pop_size, num_tasks, num_workers))
    pop[np.repeat(np.arange(pop_size), num_tasks), np.tile(np.arange(num_tasks), pop_size), idx] = 1
    return pop

def mutate(pop,mut_prob):
    return

def feasible(pop,calls_max):
    for i in range(pop.shape[0]): # iterate over population members
        for j in range(pop.shape[1]): # iterate over solution tasks
            if sum(pop[i,j]) == 0:  # select random worker if task not assigned
                pop[i,j,np.random.randint(0, num_workers)] = 1
            elif sum(pop[i,j]) > 1: # pick from assigned workers if multiply assigned
                idx = np.random.choice(np.nonzero(pop[i,j])[0])
                pop[i,j] = 0
                pop[i,j,idx] = 1
    
    for i in range(pop.shape[0]): # iterate over population members
        for k in range(pop.shape[2]): # iterate over workers
          num_calls = pop[i].sum(axis=0) # compute calls per worker
          if (overage := num_calls[k] - calls_max) > 0: # check if worker assigned excess calls
              wrkr_avail_calls = calls_max - num_calls # compute workers' remaining capacity
              wrkr_avail = wrkr_avail_calls > 0 # create Boolean indicate of free workers
              for w,wrkr in enumerate(wrkr_avail): # reassign worker excess calls
                  if wrkr:
                    # reassign calls to worker w
                    num_reassign = int(min(overage, wrkr_avail_calls[w])) 
                    idx_reassign = np.random.choice(np.arange(num_tasks)[pop[i,:,k]==1],size=num_reassign,replace=False)
                    pop[i][idx_reassign,w] = 1
                    pop[i][idx_reassign,k] = 0
                    # recompute overage for worker k
                    overage -= num_reassign
        if np.any(pop[i].sum(axis=0) > calls_max):
            print('error')
    return 

def fit_calc(task_time, pop):
    #return (task_time * pop).sum(axis=(1,2))
    return np.einsum('ijk,jk->i', pop, task_time)

def select(fit, mode, q, elitism, num_elite=5):
    
    if mode == 'proportional':
        #prob = (fit.max() - fit)/(fit.max() - fit).sum()
        prob = (1/fit)/(1/fit).sum()
    elif mode == 'rank_linear':
        rank = np.zeros(pop.shape[0])
        rank[np.argsort(fit)] = np.flip(np.arange(pop.shape[0]))
        prob = (1 + rank)/(1+rank).sum()
    elif mode == 'rank_nonlinear':
        if q>1 or q<0:
            print(f'Error in specifying q: {q}')
        else:
            rank = np.zeros(pop.shape[0])
            rank[np.argsort(fit)] = np.arange(pop.shape[0])
            prob = q**rank/(q**rank).sum()
    else:
        print(f'Error in specifying selection mode: {mode}')
    
    ''' old rank-linear 
    # Use rank-linear for selection
    rank = np.empty_like(fitness)
    order = np.argsort(fitness)
    # Rank in descending order
    rank[order] = fitness.shape[0] - np.arange(fitness.shape[0])
    prob = 2 * rank.cumsum()/(fitness.shape[0] * (fitness.shape[0] + 1))
    rv = np.random.random(size=2*fitness.shape[0])
    parents = np.sum(rv[:,np.newaxis] > prob,axis=1) '''
    
    if elitism:
        parents = np.random.choice(np.arange(pop.shape[0]), size=(2*pop.shape[0]), p = prob)
        pop2save = np.argsort(fit)[-5:]
    else:
        parents = np.random.choice(np.arange(pop.shape[0]), size=(2*pop.shape[0]), p = prob)
        pop2save = np.array([])
    return parents, pop2save

def crossover(pop, parents, elitism, pop2save):
    
    cross_pt = np.random.randint(0, pop[0].shape[0], size=(pop.shape[0]-pop2save.shape[0],))
    pop_new = []
    shape = pop.shape
    
    for i,cpt in enumerate(cross_pt):
        pop_new.append(pop[parents[2*i]][:cpt,:])
        pop_new.append(pop[parents[2*i+1]][cpt:,:])
    pop_new = np.concatenate(pop_new)
    pop_new = pop_new.reshape((-1, *shape[1:]))
    if elitism:
        pop_new = np.concatenate((pop_new,pop[pop2save].copy()), axis=0)
    pop[0] = pop_new[0]
    pop[1:] = pop_new[1:]
    
    return


def crossover_col(pop, parents, elitism, pop2save):
    
    cross_pt = np.random.randint(0, pop[0].shape[1], size=(pop.shape[0]-pop2save.shape[0],))
    pop_new = []
    shape = pop.shape
    
    for i,cpt in enumerate(cross_pt):
        pop_new.append(pop[parents[2*i]][:,:cpt])
        pop_new.append(pop[parents[2*i+1]][:,cpt:])
    pop_new = np.concatenate(pop_new, axis=1)
    pop_new = pop_new.reshape((-1, *shape[1:]))
    if elitism:
        pop_new = np.concatenate((pop_new,pop[pop2save].copy()), axis=0)
    pop[0] = pop_new[0]
    pop[1:] = pop_new[1:]
    
    return


def crossover_flat(pop, parents, elitism, pop2save):
    cross_pt = np.random.randint(0, pop[0].size, size=(pop.shape[0]-pop2save.shape[0],))
    pop_new = []
    shape = pop.shape
    
    for i,cpt in enumerate(cross_pt):
        pop_new.append(pop[parents[2*i]].flatten()[:cpt])
        pop_new.append(pop[parents[2*i+1]].flatten()[cpt:])
    pop_new = np.concatenate(pop_new)
    pop_new = pop_new.reshape((-1, *shape[1:]))
    if elitism:
        pop_new = np.concatenate((pop_new,pop[pop2save].copy()), axis=0)
    pop[0] = pop_new[0] # this and the next statement to avoid creating a function scope pop
    pop[1:] = pop_new[1:]
    
    return


## Parameters
pop_size = 2000       # population size
mutate_prob = 0.002 # 0.001 # mutation probability of a task
num_gen = 200        # number of generations
calls_max = 45
q = 0.999
select_mode = 'rank_linear' #'proportional' #'rank-nonlinear'
elitism = False
results = []
rep=0
num_elite = 5

start = time.time()

# Input task time matrix
tt = np.genfromtxt('task_time_data.csv', delimiter=',').astype(np.int16)
num_tasks, num_workers = tt.shape

# Generate initial population
pop = pop_gen(pop_size, num_tasks, num_workers)
fitness = fit_calc(tt, pop)
results.append((fitness.min(),fitness.min(),fitness.mean()))


for i in range(num_gen):
    # execute one generation
    parents,pop2save = select(fitness, select_mode, q, elitism, num_elite)
    #crossover(pop, parents, elitism, pop2save)
    #crossover_col(pop, parents, elitism, pop2save)
    crossover_flat(pop, parents, elitism, pop2save)
    mutate(pop,mutate_prob)
    feasible(pop,calls_max)
    fitness = fit_calc(tt, pop)
    results.append((fitness.min(),min(fitness.min(),results[-1][1]),fitness.mean()))
    print(results[-1][1])
    

results= np.array(results)
np.savetxt(f'results/{select_mode}_{pop_size}_{num_gen}_{rep}_'+'crossflat'+'.txt',results)
print(f'Execution time: {time.time()-start} seconds')
    