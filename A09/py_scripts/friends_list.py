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
    '''
    Read in data in csv format. From this data, build a dictionary with
    all users and their information contained within. 
    '''

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

def count_ages(user_dict):
    '''
    For checking the distribution of ages
    '''

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



def allot_quota(user_dict,ranges):
    '''
    Used to assign each user some number of friends
    25% of users will have < 10 friends
    25% will have 10-25 friends
    25% will have 26-100 friends
    25% will have > 100 friends
    '''

    max_friends_list = []
    # Outer loop iterations * inner loop iterations = len(user_dict)
    for i in range(int(len(user_dict)/len(ranges))):
        for j in range(len(ranges)):
            max_friends_list.append(random.randint(ranges[j][0]+1, ranges[j][1]+1))

    random.shuffle(max_friends_list)

    # Assign each user a friend count
    for i in range(0, len(user_dict) - 1):
        i = str(i)
        user_dict[i]['f_left'] = max_friends_list[int(i)]
        user_dict[i]['friends'] = []
        user_dict[i]['max'] = max_friends_list[int(i)]

def make_friends(users):
    '''
    An algorithm for building every user's friends list. This loops through
    all users in the dictionary.

    Step 1: randomly select potential friend
    Successful try:
    Step 2: potential friend can accept more friends, both users add each other
    Step 3: decrement f_left for both users
    Step 4: try again
    Unsuccessful try:
    Step 2: potential friend is already a friend or cannot accept more friends,
        increment failure counter
    Step 3: try again

    The loop stops when f_left = 0 or fails = 10 to avoid trying forever.
    '''
    print("Starting friend finder...")
    start = timer()
    # TODO: Fix dict len error. It is 1 too big
    for user in range(0, len(users) - 2):
        fails = 0
        user = str(user)
        # Loops until user hits friend quota or fails too many times
        while (users[user]['f_left'] > 0 and fails < 100):
            # Get index of potential friend
            potential = int((len(users) - 1) * random.random())
            potential = str(potential)
            if(users[potential]['f_left'] > 0 and potential not in users[user]['friends']):
                # Add both users to each other's friends list
                users[user]['friends'].append(potential)
                users[potential]['friends'].append(user)
                # Decrement friends left list
                users[user]['f_left'] -= 1
                users[potential]['f_left'] -= 1
            else:
                fails += 1

    end = timer()
    elapsed = end - start
    print(f"Matched friends for {elapsed} seconds.")

def make_friends_test():
    pass

def print_to_json(user_dict):
    print("Writing users to json file...")
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(user_dict, f)

if __name__ == '__main__':
    user_list = {}
    user_list = build_dict()

    ranges = [[3,10],[11,25],[26,100],[101,250]]
    allot_quota(user_list, ranges)

    print(len(user_list))

    make_friends(user_list)

    print("User 0:")
    print(user_list['0']['friends'])
    print(user_list['0']['max'])
    print(user_list['0']['f_left'])

    print("User 9999:")
    print(user_list['9999']['friends'])
    print(user_list['9999']['max'])
    print(user_list['9999']['f_left'])

