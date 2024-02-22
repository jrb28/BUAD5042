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

def make_feasible(pop,calls_max):
    for i in range(pop.shape[0]):
        for j in range(pop.shape[1]):
            if sum(pop[i,j]) == 0:
                pop[i,j,np.random.randint(0, num_workers)] = 1
            elif sum(pop[i,j]) > 1:
                idx = np.random.choice(np.nonzero(pop[i,j])[0])
                pop[i,j] = 0
                pop[i,j,idx] = 1
    
    for i in range(pop.shape[0]):
        for k in range(pop.shape[2]):
          num_calls = pop[i].sum(axis=0)
          if (overage := num_calls[k] - calls_max) > 0:
              wrkr_avail_calls = calls_max - num_calls
              wrkr_avail = wrkr_avail_calls > 0
              for w,wrkr in enumerate(wrkr_avail):
                  if wrkr:
                    num_reassign = int(min(overage, wrkr_avail_calls[w]))
                    idx_reassign = np.random.choice(np.arange(num_tasks)[pop[i,:,k]==1],size=num_reassign,replace=False)
                    pop[i][idx_reassign,w] = 1
                    pop[i][idx_reassign,k] = 0
                    overage -= num_reassign
        if np.any(pop[i].sum(axis=0) > calls_max):
            print('error')
    return 

def fit_calc(task_time, pop):
    return (task_time * pop).sum(axis=(1,2))

def select(fit, mode, q, elitism, num_elite=5):
    
    if mode == 'proportional':
        epsilon = 0.001
        prob = (fit.max() - fit + epsilon)/(fit.max() - fit + epsilon).sum()
        #prob = (1/fit)/(1/fit).sum()
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

def crossover(pop, parents, elitism, pop2save, mode):
    if mode=='task':
        cross_pt = np.random.randint(0, pop[0].shape[0], size=(pop.shape[0]-pop2save.shape[0],))
        pop_new = []
        shape = pop.shape
        
        for i,cpt in enumerate(cross_pt):
            pop_new.append(pop[parents[2*i]][:cpt,:])
            pop_new.append(pop[parents[2*i+1]][cpt:,:])
        pop_new = np.concatenate(pop_new)
        
    elif mode=='worker':
        cross_pt = np.random.randint(0, pop[0].shape[1], size=(pop.shape[0]-pop2save.shape[0],))
        pop_new = []
        shape = pop.shape
        
        for i,cpt in enumerate(cross_pt):
            pop_new.append(pop[parents[2*i]][:,:cpt])
            pop_new.append(pop[parents[2*i+1]][:,cpt:])
        pop_new = np.concatenate(pop_new, axis=1)
        
    elif mode=='flatten':
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


# Parameters
#pop_size = 2000       # population size
mutate_prob = 0.002 # 0.001 # mutation probability of a task
num_gen = 250        # number of generations
calls_max = 45
#q = 0.999
#select_mode = 'rank_linear' #'proportional' #'rank_nonlinear'
pop_sizes = [2000] #[1000,2000] 
select_alts = ['proportional'] #['proportional','rank_linear','rank_nonlinear'] 
qs = [[1]] #[[1],[1],[0.9,0.95,0.97,0.999]] 
elitism = [False]
crossover_mode = 'flatten' #['task', 'worker', 'flatten']
num_elite = 5
reps = 10 #2

start = time.time()

# Input task time matrix
tt = np.genfromtxt('task_time_data.csv', delimiter=',').astype(np.int16)
num_tasks, num_workers = tt.shape

results = []

for j,select_mode in enumerate(select_alts):
    for pop_size in pop_sizes:
        for e in elitism:
            for q in qs[j]:
                results.append([select_mode, crossover_mode, pop_size, e, q])
                for rep in range(reps):
                    data_run = []
                    # Generate initial population
                    pop = pop_gen(pop_size, num_tasks, num_workers)
                    fitness = fit_calc(tt, pop)
                    data_run.append((fitness.min(),fitness.min(),fitness.mean()))
                               
                    for i in range(num_gen):
                        # execute one generation
                        parents,pop2save = select(fitness, select_mode, q, e, num_elite)
                        crossover(pop, parents, e, pop2save, crossover_mode)
                        make_feasible(pop,calls_max)
                        mutate(pop,mutate_prob)
                        fitness = fit_calc(tt, pop)
                        data_run.append((fitness.min(),min(fitness.min(),data_run[-1][1]),fitness.mean()))
                        print(data_run[-1][1])
                        
                    
                    results[-1].append(data_run[-1][1])
                    data_run= np.array(data_run)
                    np.savetxt(f'results/{select_mode}_{pop_size}_{num_gen}_{crossover_mode}_{"_elite" if e else ""}_{int(q*1000)}_{rep}.txt',data_run)
                    print(f'Execution time: {time.time()-start} seconds')

results = '\n'.join([','.join([str(y) for y in x]) for x in results])
with open('results/result_crossover1.csv', 'w') as f:
    f.write(results)