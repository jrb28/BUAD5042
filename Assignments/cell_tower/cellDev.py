# -*- coding: utf-8 -*-
"""
Spyder Editor
"""

import mysql.connector as mySQL
import re

""" global MySQL settings """
mysql_user_name = ''
mysql_password = ''
mysql_ip = ''
mysql_db = 'cell_tower'

def checkBudget(towers,budget):
    """ contents is expected as a dictionary of the form {tower_id:(cost,calls), ...} """
    """ This function returns True if the cell tower construction plan is within budget; False otherwise """
    load = 0
    if isinstance(towers,dict):
        for this_key in towers.keys():
            load = load + towers[this_key][0]
        if load <= budget:
            return True
        else:
            return False
    else:
        print("function checkBudget() requires a dictionary")

def compute_added_calls(towers):
    value = 0.0
    if isinstance(towers,dict):
        for this_key in towers.keys():
            value = value + towers[this_key][1]
        return(value)
    else:
        print("function compute_added_calls() requires a dictionary")

def cell_algo(towers,budget):
    """ You write your heuristic cell tower algorithm in this function using the argument values that are passed
             towers: a dictionary of the possible cell towers
             budget: budget for adding cell towers, which total cost cannot exceed
    
        Your algorithm must return two values as indicated in the return statement:
            my_username: your WM username
            towers_to_pick: list containing keys (integers) of the towers you want to construct
                            The integers refer to keys in the towers dictionary. 
   """
        
    my_user_name = "no_name"   # replace string with your username
    my_nickname = 'nickname'   # if you chose, enter a nickname to appear instead of your username
    towers_to_pick = []        # use this list for the indices of the towers you select
    investment = 0.0           # use this variable, if you wish, to keep track of how much of the budget is already used
    tot_calls_added = 0.0      # use this variable, if you wish, to accumulate total calls added given towers that are selected
        
    ''' Start your code below this comment '''
    
    
    ''' Finish coding before this comment '''
    
    return my_user_name, towers_to_pick, my_nickname    

def getDBDataList():
    cnx = db_connect()
    cursor = cnx.cursor()
    #cursor.execute(commandString)
    cursor.callproc('spGetProblems')
    items = []
    for result in cursor.stored_results(): #list(cursor):
        for item in result.fetchall():
            items.append(item[0])
        break
    cursor.close()
    cnx.close()
    return items
   
""" db_get_data connects with the database and returns a dictionary with the problem data """
def db_get_data(problem_id):
    cnx = db_connect()
                        
    cursor = cnx.cursor()
    cursor.callproc("spGetBudget", args=[problem_id])
    for result in cursor.stored_results():
        knap_cap = result.fetchall()[0][0]
        break
    cursor.close()
    cnx.close()
    cnx = db_connect()
    cursor = cnx.cursor()
    cursor.callproc('spGetData',args=[problem_id])
    items = {}
    for result in cursor.stored_results():
        blank = result.fetchall()
        break
    for row in blank:
        items[row[0]] = (row[1],row[2])
    cursor.close()
    cnx.close()
    return knap_cap, items
    
def db_connect():
    cnx = mySQL.connect(user=mysql_user_name, passwd=mysql_password,
                        host=mysql_ip, db=mysql_db)
    return cnx

def print_find(f_name):
    #print(__file__)
    f_name = f_name[:]
    f_name = f_name.replace('()','')
    
    with open(__file__, 'r') as f:
        code = f.readlines()
        
    i = 0
    while not re.search('def\s'+f_name,code[i]) and i < len(code) - 1:
        i += 1
    if i == len(code) - 1:
        msg = 'Function %s() is missing from this code' % f_name
    else:
        i += 1
        msg = None
        while re.search('^\s+', code[i]):
            if not re.search('\s+#', code[i]) and re.search('print\(', code[i]):
                #print('Please remove or comment out the print statement in your function code before submission:', code[i])
                msg += 'Please remove or comment out the print statement in your %s() function code before submission: %s\n' % (f_name, code[i].strip(),)
            i += 1
    
    return msg
    
""" Error Messages """
error_bad_list_key = """ 
The towers_to_pick list received from cell_algo() either contained an element that was not a valid tower key or a valid tower key was included multiple times. Please check the towers_to_pick list that your cell_algo() function is returning for these errors. Other errors may also exist.
"""
error_response_not_list = """
cell_algo() returned a response for towers to be built that was not of the list data type.  Scoring will be terminated.  Other errors may also exist.   """

error_over_budget = '''Cell towers in towers_to_pick exceed the budget. '''
silent_mode = False    # use this variable to turn on/off appropriate messaging depending on student or instructor use

''' Get problem IDs to solve '''
problems = getDBDataList() 

''' First, check to ensure that function cell_algo() exists '''
''' Print message if no function; otherwise: solve problems in database '''
msg = print_find('cell_algo')
if msg:
    print('\n\n' + msg)
else:
    print('Cell Tower Problems to Solve:', problems)
    for problem_id in problems:
        print("Cell Tower Problem ", str(problem_id)," ....")
        towers_selected = {}
        budget, towers = db_get_data(problem_id)
        #finished = False
        errors = False
        response = None
        
        #print('function')
        team_num, response, nicname = cell_algo(towers.copy(),budget)
        if isinstance(response,list):
            for this_key in response:
                if this_key in towers.keys():
                    towers_selected[this_key] = towers[this_key]
                    del towers[this_key]
                else:
                    errors = True
                    if silent_mode:
                        status = error_bad_list_key #"Cell tower ID not valid (other errors may exist)"
                    else:
                        print("Problem " + str(problem_id) + ': ' + error_bad_list_key)
                    #finished = True
        else:
            errors = True
            if silent_mode:
                status = "Problem "+str(problem_id) + ': ' + error_response_not_list
            else:
                print(error_response_not_list)
                    
        if errors == False:
            budget_ok = checkBudget(towers_selected,budget)
            if budget_ok:
                towers_result = compute_added_calls(towers_selected)
                print("Problem " + str(problem_id) + ': Selected tower locations are within budget, Total Calls Added : ' + str(towers_result))
            else:
                print("Problem " + str(problem_id) + ': ' + error_over_budget)

