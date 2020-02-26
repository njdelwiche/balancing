import pandas as pd
import numpy as np
import math
import random
from random import randint
import sys

roster = pd.read_csv(sys.argv[2])

## will use this vairable later for double checking
roster_backup = pd.read_csv('data/2020_roster.csv')

total = len(roster)
num_groups = sys.argv[3]

groups_storage = []

## storing the final group values
for x in range(num_groups):
    groups_storage.append(x + 1)

## setting up the groups column for later
roster['Group'] = 0

## select your criteria
criteria_list = ['Gender', 'Section']

## will store the groups in a list
agg_groups= []

def modify(original,unbalanced, item, add):
    
    rand_int = randint(0,total//num_groups - 1)
    
    if add == False:
        
        ## continue searching for a random to-be-swapped or swapping item if they are unsuitable  
        while original.iloc[rand_int][item] != unbalanced or roster.iloc[rand_int][item] == unbalanced:

            rand_int = randint(0,total//num_groups - 1)
    else:
        
        ## continue searching for a random to-be-swapped or swapping item if they are unsuitable  
        while roster.iloc[rand_int][item] != unbalanced:

            rand_int = randint(0,total//num_groups - 1)

    
    ## swap two random items
    original.iloc[rand_int], roster.iloc[rand_int] = roster.iloc[rand_int].copy(), original.iloc[rand_int].copy()

def check_all(group, desired):
    
    while True:

        counter = 0
        
        ## go through the values of the balancing criteria 
        for key in desired.keys():              
                        
            ## finding the actual distribution of a group
            actual = make_dict(group,criteria_list, upper=False)

            try:

                ## if there are more than maximally allowed
                if actual[key][0] > desired[key][0]:

                    counter += 1

                    ## swap the over-weighted item
                    modify(group,key, actual[key][1], add = False)
                
                ## if there are fewer than minimally allowed
                elif actual[key][0] < desired[key][0] - 1:
                    
                    counter += 1
                    
                    ## add the item that is underbalanced
                    modify(group, key, desired[key][1], add = True)
                                               
            except Exception as e:
                
                ## if the sample has 0 of the desired keys the search will run an error
                    
                if desired[key][0] > 1 and key not in actual:
                        
                    counter += 1
                    
                    ## add the item that is underbalanced
                    modify(group, key, desired[key][1], add = True)
                        
                else :
                    print(e)
                                            
        ## if it got through all the criteria and balacned distributions with the counter still at 0
        ## then it is balanced 
        if counter == 0:
            print('BALANCED')
            break


def make_dict(group, criteria,upper):
    my_dict = {}
    
    for criterion in criteria:
        
        uniques = group[criterion].value_counts()

        for x in uniques.index:
            
            ## do this if you are trying to get the maximal allotments
            if upper == True:
                
                ## find the upper ceiling of the criteria
                max_accepted = math.ceil(uniques[x]/num_groups)
                my_dict[x] =[max_accepted, criterion]

            else:
                my_dict[x] = [uniques[x], criterion]
            
    return my_dict


## make the dictionary with all the correct values for the criteria selected
desired_dict = make_dict(roster, criteria_list, upper = True)



get_ipython().run_cell_magic('time', '', 'for x in range(num_groups - 1):\n    \n    ## randomly create the groups\n    bit = roster.sample(total//num_groups);\n    agg_groups.append(bit)\n    \n    ## delete that part of the dataframe\n    roster.drop(bit.index, inplace=True)\n    \n    check_all(agg_groups[x], desired_dict)\n    \n    print(x)\n    \nagg_groups.append(roster.sample(total//num_groups))')



## assign the labels to the newly balanced groups
for x in agg_groups:
    x['Group'] = groups_storage.pop(0)


#merging all the groups together 
my_data = pd.concat(agg_groups)

print(roster_backup['Section'].value_counts())

## final check that the new spreadsheet has the same overall distribution as the original  
for x in criteria_list:
    print(roster_backup[].value_counts() == my_data[x].value_counts())

## save the csv file
my_data.to_csv("data/{}.csv".format('2020_final'), index=False)


## checking the criteria distributions that should be balanced
[[x[y].value_counts().sort_index() for x in agg_groups] for y in criteria_list]
