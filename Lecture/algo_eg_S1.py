# -*- coding: utf-8 -*-
"""
Created on Tue Dec 20 14:12:18 2022

@author: jrbrad
"""

''' Get location and travel path data '''
# Get location data
with open('location_info.csv', 'r') as f:
    locs = f.readlines()

# Prepare headings for location data
head_locs = locs[0].strip().split(',')
del locs[0]    

# Prepare location information list
for i in range(len(locs)):
    locs[i] = locs[i].strip().split(',')
    for j in range(2,len(locs[i])):
        locs[i][j] = float(locs[i][j])
        
locs = {x[1].strip():{head_locs[i].strip():x[i] for i in range(len(x)) if i != 1} for x in locs}

# Get feasible travel path information
links = {}
with open('links.csv', 'r') as f:
    data = f.readlines()
head_links = data[0].strip().split(',')
del data[0]

# Prepare feasible links data
for i in range(len(data)):
    data[i] = data[i].strip().split(',')
    links[head_links[i]] = {head_links[k]:eval(data[i][k].strip()) for k in range(len(data[i]))}

''' Initialize
      - Set starting location to 'W'
      - Initialize path and path distance variables '''
loc_cur = 'W'
loc_dest = 'LA'
path = [loc_cur]
dist = 0.0  
        
while loc_cur != loc_dest:
    ''' Find possible next destinations: 
          - where connections exist 
          - and have not been visited '''
    locs_next = [(k,v) for k,v in links[loc_cur].items() if v and k not in path]
    
    ''' Identify closest next destination 
          - set current location to next location selected 
          - Update path
          - Update distance  '''
    ''' sort next destination list, pick 0th element '''
    locs_next.sort(key=lambda x:x[1])
    path.append(locs_next[0][0])
    dist += locs_next[0][1]
    loc_cur = locs_next[0][0]
    
print(f'Travel path: {path}; Total miles: {dist} miles')