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


''' Initialization '''
# Initialize total distance
dist = 0.0
# Initialize current location
loc_cur = 'W'
# initialize destination
loc_fin = 'LA'
# Initialize path
route = [loc_cur]

'''Loop until we get to LA '''
while loc_cur != loc_fin:
    ''' Determine next feasible locations 
        - mileage in data
        - location has not yet been visited '''
    locs_next = [(mileage, city) for city,mileage in links[loc_cur].items() if mileage and city not in route]
    
            
    ''' Of next possible locations, find closest
          - append closest next location to path 
          - update total distance     
          - update current location '''
    locs_next.sort()
    route.append(locs_next[0][1])
    dist += locs_next[0][0]
    loc_cur = locs_next[0][1]

    
print(f'Travel path: {route}; Total miles: {dist} miles')