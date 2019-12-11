#!/usr/bin/env python3

#****************************************************************************
# A script for building a list of friends for a redis cluster.
#
# Usage: ./friends_list.py 
#****************************************************************************

import json
import pprint
import random
import io
import markovify
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
    percentage = [0] * 7

    # Count the frequency of ages in range
    for i in range(1, len(user_dict) - 1):
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

    total_pop = sum(age_dist)
    print("Age distributions: ")
    for i in range(len(age_dist)):
        percentage[i] = (age_dist[i] / total_pop) * 100
        print(f"{round(percentage[i],2)}%")

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

def make_friends(users, tries=1000):
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

    The loop stops when f_left = 0 or fails = number of tries allowed to 
    avoid trying forever.
    '''
    print("Starting friend finder...")
    start = timer()
    # TODO: Fix dict len error. It is 1 too big
    for user in range(0, len(users) - 2):
        fails = 0
        user = str(user)
        # Loops until user hits friend quota or fails too many times
        while (users[user]['f_left'] > 0 and fails < tries):
            # Get index of potential friend
            # len(users) - 1 * random.random() is used instead of 
            # random.ranint(0,len(users)-1) because it is much faster
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

def make_friends_test(users):
    '''
    A test to measure the effectiveness of the friend-finding algorithm
    Compare the average expected friend count vs. the actual friend count
    '''
    expected_sum = 0
    actual_sum = 0
    # TODO: fix dict len error. It is 1 too big. Change test
    for user in range(0, len(users) - 2):
        user = str(user)
        expected_sum += users[user]['max']
        actual_sum += len(users[user]['friends'])
    
    expected_average = expected_sum / (len(users) - 1)
    actual_average = actual_sum / (len(users) - 1)

    print(f"Average expected friend count: {expected_average}")
    print(f"Actual average friend count: {actual_average}")

def make_model():
    '''
    Using the markovify module, which can be found at https://github.com/jsvine/markovify,
    a model is built from a text file of short conversations. This model will generate
    the messages used to simulate message traffic in our social media network.
    '''
    # Build the model from text conversations
    infile = 'conversations.txt'
    with io.open(infile, 'r', encoding='utf-8') as f:
        text = f.read()

    text_model = markovify.Text(text)

    return text_model

def build_messages(text_model, messages, users, num_mess=1000):
    '''
    This function takes messages generated by the markovify module,
    assigns them a sender ID and reciever ID, and packages the result
    into a dictionary. By default, build_messages creates 1000 messages.

    Step 1: Pick a random user and assign as sender
    Step 2: Pick a random friend in user's friends list to assign
        as the receiver
    Step 3: Insert into messages dictionary
    '''
    
    for i in range(num_mess):
        # Select a random user to be the sender
        send = int((len(users) - 1) * random.random())
        send = str(send)
        # Select a random user from the sender's friends list to be
        # the receiver
        index = int((len(users[str(send)]['friends']) - 1) * random.random())
        rec = str(users[send]['friends'][index])

        # Generate markovified message
        message = text_model.make_sentence()
        # Place message in dictionary
        messages['message{}'.format(i)] = {'send': send, 'rec': rec, 'message': message}

def users_to_json(user_dict):
    '''
    Prints the users dictionary to a json file
    '''
    print("Writing users to json file...")
    with open('user_data.json', 'w', encoding='utf-8') as f:
        json.dump(user_dict, f)

def messages_to_json(messages):
    '''
    Prints the messages dictionary to a json file
    '''
    print("Writing messages to json file...")
    with open('message_data.json', 'w', encoding='utf-8') as f:
        json.dump(messages, f)
    

def redis_plain_users():
    '''
    Prints plain text redis commands for inserting the user data generated
    in this script into a redis instance.
    '''
    pass

def redis_plain_messages():
    '''
    Prints plain text redis commands for inserting the message data generated
    in this script into a redis instance.
    '''
    pass


if __name__ == '__main__':
    text_model=None
    messages = {}
    user_list = {}
    ranges = [[3,10],[11,25],[26,100],[101,250]]

    # Build user list from csv data
    user_list = build_dict()
    # Give each user a maximum number of potential friends
    allot_quota(user_list, ranges)
    # Build a list of friends for each user
    make_friends(user_list)
    # Create simulated message traffic
    text_model = make_model()
    build_messages(text_model, messages, user_list)

    '''
    Some tests:

    print(len(user_list))
    
    print("User 0:")
    print(user_list['0']['friends'])
    print(user_list['0']['max'])
    print(user_list['0']['f_left'])

    print("User 9999:")
    print(user_list['9999']['friends'])
    print(user_list['9999']['max'])
    print(user_list['9999']['f_left'])

    print("Average friend test")
    make_friends_test(user_list)
    count_ages(user_list)
    '''