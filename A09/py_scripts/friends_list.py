#!/usr/bin/env python3

#****************************************************************************
# A script for building a list of friends for a redis cluster.
#
# Usage: ./friends_list.py 
#****************************************************************************

import json
import pprint
import random
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
    print("Building dictionary...")
    users = {}

    start = timer()
    for line in input:
        # Read the line and clean it up
        line = line.split(sep=",")
        line[-1] = line[-1].rstrip('\n')

        users[line[0]] = {}
        for j in range(1,len(line)):
            users[line[0]][header[j]] = line[j]

    end = timer()
    elapsed = end - start

    print(f"Dictionary built in {elapsed} seconds.")

    input.close()
    return users

# For checking the distribution of ages
def count_ages(user_dict):
    # Initialize a list with five elements for our seven categories
    age_dist = [0] * 7

    # Count the frequency of ages in range
    for i in range(1, len(user_dict)):
        age = user_dict[str(i)]['age']
        age = int(age)
        if (age >= 13 and age <= 17):
            age_dist[0] += 1
        elif (age >= 18 and age <= 24):
            age_dist[1] += 1
        elif (age >= 25 and age <= 34):
            age_dist[2] += 1
        elif (age >= 35 and age <= 44):
            age_dist[3] += 1
        elif (age >= 45 and age <= 54):
            age_dist[4] += 1
        elif (age >= 55 and age <= 64):
            age_dist[5] += 1
        elif (age >= 65):
            age_dist[6] += 1

    return age_dist

# Used to assign each user some number of friends
'''
25% of users will have < 10 friends
25% will have 10-25 friends
25% will have 26-100 friends
25% will have > 100 friends
'''
def allot_quota(user_dict,ranges):
    max_friends_list = []
    # Outer loop iterations * inner loop iterations = len(user_dict)
    for i in range(int(len(user_dict)/len(ranges))):
        for j in range(len(ranges)):
            max_friends_list.append(random.randint(ranges[j][0]+1, ranges[j][1]+1))

    random.shuffle(max_friends_list)

    # Assign each user a friend count
    for i in range(0, len(user_dict) - 1):
        i = str(i)
        user_dict[i]['allowed'] = max_friends_list[int(i)]
        user_dict[i]['friends'] = []
        user_dict[i]['max'] = max_friends_list[int(i)]

def print_to_json(user_dict):
    print("Writing users to json file...")
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(user_dict, f)

if __name__ == '__main__':
    user_list = {}
    user_list = build_dict()

    ranges = [[3,10],[11,25],[26,100],[101,250]]
    allot_quota(user_list, ranges)

    print(temp_user2['0'])

    #print_to_json(user_list)

