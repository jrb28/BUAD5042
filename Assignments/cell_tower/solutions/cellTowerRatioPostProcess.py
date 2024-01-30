def cell_algo(towers, budget):
    """ You write your heuristic knapsack algorithm in this function using the argument values that are passed
             items: is a dictionary of the items no yet loaded into the knapsack
             knapsack_cap: the capacity of the knapsack (volume)
    
        Your algorithm must return two values as indicated in the return statement:
             my_team_number_or_name: if this is a team assignment then set this variable equal to an integer representing your team number;
                                     if this is an indivdual assignment then set this variable to a string with you name
            items_to_pack: this is a list containing keys (integers) of the items you want to include in the knapsack
                           The integers refer to keys in the items dictionary. 
   """
    
    my_user_name = 'jrbrad'
    my_nickname = 'nickname'
    towers_to_pick = []    # use this list for the indices of the selected towers
    investment = 0.0       # variable to keep track of investment committed to selected towers
    calls_added = 0.0  # variable to keep track of total number of calls covered by selected towers 
    
    tow = [(k,v[0],v[1],v[1]/v[0]) for k,v in towers.items()]
    tow.sort(key=lambda x:x[3], reverse = True)
    
    for tow_id,cost,calls,_ in tow:
        if investment + cost <= budget:
            towers_to_pick.append(tow_id)
            investment += cost
            calls_added += calls
            
    ''' Postprocessing: remove some selected towers '''
    n = 1 # number of selected towers to remove
    
    tow = [t for t in tow if t[0] not in towers_to_pick[-n:]]
    ttp2 = []
    investment = 0.0
    calls_added2 = 0.0
    for tow_id,cost,calls,_ in tow:
        if investment + cost <= budget:
            ttp2.append(tow_id)
            investment += cost
            calls_added2 += calls
    
    if calls_added2 > calls_added:
        return my_user_name, ttp2, my_nickname
    else:
        return my_user_name, towers_to_pick, my_nickname
