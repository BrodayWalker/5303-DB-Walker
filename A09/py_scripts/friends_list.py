#!/usr/bin/env python3

#****************************************************************************
# A simple script for building a list of friends for a redis cluster.
#
# Usage: ./friends_list.py 
#****************************************************************************

import json
from timeit import default_timer as timer

def build_dict():
    # Open the input file
    input = open('data.csv', 'r')

    # The first line contains the name of each field
    header = input.readline() # Read the line
    header = header.split(sep=",") # Make into list
    header[-1] = header[-1].rstrip() # Strip trailing new line

    # Build a dictionary of users using the fields given in the header and the
    # data provided in the line
    print("Building hash...")
    records = 0
    users = {}
    i = 1

    start = timer()
    for line in input:
        # Read the line and clean it up
        line = line.split(sep=",")
        line[-1] = line[-1].rstrip()

        # Check to see if the user is already in the hash
        if line[0] not in users:
            # Iterate through list to build the hash
            users[line[0]] = {}
            for j in range(1,len(line)):
                users[line[0]][header[j]] = line[j]
            records += 1
        else:
            pass
        i += 1
    end = timer()
    elapsed = end - start

    print(f"{records} records inserted in hash in {elapsed} seconds.")
    return users

def allot_quota(user_dict):
    pass

def print_to_json(user_dict):
    print("Writing users to json file...")
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(user_dict, f)

if __name__ == '__main__':
    user_list = {}
    user_list = build_dict()
    print_to_json(user_list)




