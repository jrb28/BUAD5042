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
        

''' Initialize route '''
loc_cur = 'W'
loc_dest = 'LA'
route = []
dist = 0

''' Iteratively select next destinations '''
while loc_cur != loc_dest:
  #locs_next = [k for k,v in links[loc_cur].items() if v and k not in route]
  ''' Initialze next stop variables '''
  loc_next = ''
  dist_next = 999999999999
  ''' find next stop with largest cosine '''
  for loc in [k for k,v in links[loc_cur].items() if v and k not in route]: #locs_next
      if links[loc_cur][loc] < dist_next and locs[loc]['miles_e'] < locs[loc_cur]['miles_e']:
          loc_next = loc
  ''' Update route '''
  route.append(loc_next)
  dist += links[loc_cur][loc_next]
  print(f'route: {route}; distance; {dist}')
  loc_cur = loc_next
    
''' Print results '''    
print(f'Travel route: {route}; Total miles: {dist} miles')