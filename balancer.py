import csv
import pandas as pd
import numpy as np
import math
import random
from random import randint
import sys

MAX_ATTEMPTS = 25
MAX_ATTEMPTS_LARGE = 500

def modify(original,unbalanced, item, add=True):    
    large_int = randint(0, len(roster) - 1)
    small_int = randint(0, len(original) - 1)
    
    if not add:
        # continue searching for a random to-be-swapped or swapping item if they are unsuitable  
        while original.iloc[small_int][item] != unbalanced or roster.iloc[large_int][item] == unbalanced:
            large_int = randint(0, len(roster) - 1)
            small_int = rand_int(0, len(original) - 1)
    else:
        # continue searching for a random to-be-swapped or swapping item if they are unsuitable  
        attempts = 0
        while roster.iloc[large_int][item] != unbalanced and attempts < MAX_ATTEMPTS_LARGE:
            attempts += 1
            large_int = randint(0, len(roster) - 1)

    # swap two random items
    original.iloc[small_int], roster.iloc[large_int] = roster.iloc[large_int].copy(), original.iloc[small_int].copy()


def check_all(group, desired, criteria_list):
    attempts = 0
    while attempts < MAX_ATTEMPTS:
        attempts += 1
        counter = 0        
        # go through the values of the balancing criteria 
        for key in desired.keys():                     
            # finding the actual distribution of a group
            actual = make_dict(group, criteria_list, upper=False)
            try:
                # if there are more than maximally allowed
                if actual[key][0] > desired[key][0]:
                    counter += 1
                    # swap the over-weighted item
                    modify(group,key, actual[key][1], add=False)
                # if there are fewer than minimally allowed
                elif actual[key][0] < desired[key][0] - 1:
                    counter += 1
                    # add the item that is underbalanced
                    modify(group, key, desired[key][1], add=True)
                                               
            except Exception as e:
                # if the sample has 0 of the desired keys the search will run an error                    
                if desired[key][0] > 1 and key not in actual:
                    counter += 1
                    # add the item that is underbalanced
                    modify(group, key, desired[key][1], add = True)
                else :
                    pass
                    #print(f"Could not find {e}, but continuing.")                                           
        # If counter still at 0 then it is balanced 
        if counter == 0:
            break


def make_dict(group, criteria, upper):
    my_dict = {}
    for criterion in criteria:
        uniques = group[criterion].value_counts()
        for x in uniques.index:
            # do this if you are trying to get the maximal allotments
            if upper == True:
                # find the upper ceiling of the criteria
                max_accepted = math.ceil(uniques[x]/num_groups)
                my_dict[x] =[max_accepted, criterion]
            else:
                my_dict[x] = [uniques[x], criterion]
    return my_dict


def run_balance():
    # setting up the groups column for later
    roster['Group'] = 0
    # will store the groups in a list
    agg_groups= []
    # make the dictionary with all the correct values for the criteria selected
    desired_dict = make_dict(roster, criteria, upper=True)

    for x in range(num_groups - 1):
        # randomly create the groups
        bit = roster.sample(total//num_groups)
        agg_groups.append(bit)
        
        # delete that part of the dataframe
        roster.drop(bit.index, inplace=True)
        check_all(agg_groups[x], desired_dict, criteria)
        print(x)
        
    agg_groups.append(roster.sample(total//num_groups))

    # assign the labels to the newly balanced groups
    for i, x in enumerate(agg_groups):
        x['Group'] = i + 1

    # merging all the groups together 
    my_data = pd.concat(agg_groups)

    # save the csv file
    my_data.to_csv(f"{sys.argv[1].strip('.csv')}_BALANCED.csv", index=False)

    # checking the criteria distributions that should be balanced
    rows = []
    for x in agg_groups:
        row = []
        for y in criteria:
            options = sorted(options_dict[y])
            values_dict = x[y].value_counts().to_dict()
            row += [values_dict.get(key) if key in values_dict else 0 for key in options]
        rows.append(row)

    # Produce CSV report of the balances
    row_list = [column_names] + rows
    with open(f'{sys.argv[1]}_REPORT.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(row_list)
    return True


if __name__ == '__main__':
    num_groups = int(sys.argv[2])
    roster = pd.read_csv(sys.argv[1])

    # select your criteria
    while True:
        try:
            criteria = input(f"Select Eligible criteria (separate by a comma for multiple): {roster.columns.values}\n").split(',')
            break
        except:
            print("Not a valid criteria")

    column_names = [] 
    for row in criteria:
        column_names += sorted(roster[row].unique().tolist())
    options_dict = {row: roster[row].unique().tolist() for row in criteria}
    total = len(roster)
    run_balance()
