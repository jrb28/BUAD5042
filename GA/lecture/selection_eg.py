# -*- coding: utf-8 -*-
"""
Created on Tue Jan  9 14:40:03 2024

@author: jrbrad
"""

import numpy as np
import matplotlib.pyplot as plt

''' Generate an array of random fitness values '''
fit = np.random.random(11)*100
np.savetxt('fit.txt', fit)
''' Sort fitness in ascending order to see probabilities 
    more clearly '''
fit = fit[np.argsort(fit)]
print(f'Fitness array: {fit}')

''' Proportional selection probabilities'''
p_p = fit/fit.sum()
#print(f'Proportional selection probabilities: {p_p}')
fig,ax = plt.subplots()
ax2 = ax.twinx()
ax2.set_ylabel('Fitness')
ax2.set_ylim(0,100)
ax.set_ylim(0,p_p.max()*(1+(100-fit.max())/fit.max()))
ax.bar(x=np.arange(p_p.shape[0]), height=p_p,color='gray', label='Selection Prob.')
ax2.plot(fit,c='b', label='Fitness')
ax.set_ylabel('Selection Probability')
ax.set_xlabel('Rank')
ax.legend(loc=6, bbox_to_anchor=(0.26, 0.605, 0.5, 0.655),frameon=False)
ax2.legend(loc=2,frameon=False)
fig.savefig('sel_prop_eg.jpg', dpi=600)
plt.show()



''' Rank-linear selection probabilities '''
r = np.arange(fit.shape[0])
p_rl = (1+r)/(1+r).sum()
#print(f'Rank-linear selection probabilities: {p_rl}')
fig,ax = plt.subplots()
ax2 = ax.twinx()
ax2.set_ylabel('Fitness')
ax2.set_ylim(0,100)
ax.set_ylim(0,p_rl.max()*(1+(100-fit.max())/fit.max()))
ax.bar(x=np.arange(p_rl.shape[0]), height=p_rl,color='gray', label='Selection Prob.')
ax2.plot(fit,c='b', label='Fitness')
ax.set_ylabel('Selection Probability')
ax.set_xlabel('Rank')
ax.legend(loc=6, bbox_to_anchor=(0.26, 0.605, 0.5, 0.655),frameon=False)
ax2.legend(loc=2,frameon=False)
fig.savefig('sel_rl_eg.jpg', dpi=600)
plt.show()



''' Rank-nonlinear selection probabilities '''
q = 0.5
r = np.flip(np.arange(fit.shape[0]))
p_nrl = q**(1+r)/(q**(1+r)).sum()
#print(f'Rank-nonlinear selection probabilities: {p_nrl}')
fig,ax = plt.subplots()
ax2 = ax.twinx()
ax2.set_ylabel('Fitness')
ax2.set_ylim(0,100)
ax.set_ylim(0,p_nrl.max()*(1+(100-fit.max())/fit.max()))
ax.bar(x=np.arange(p_nrl.shape[0]), height=p_nrl,color='gray', label='Selection Prob.')
ax2.plot(fit,c='b', label='Fitness')
ax.set_ylabel('Selection Probability')
ax.set_xlabel('Rank')
ax.legend(loc=6, bbox_to_anchor=(0.26, 0.605, 0.5, 0.655),frameon=False)
ax2.legend(loc=2,frameon=False)
fig.savefig('sel_rnl_eg.jpg', dpi=600)
plt.show()


''' Rank-linear selection probability alternatives '''
r = np.argsort(fit)
p_rl_0 = (1+r)/(1+r).sum()






