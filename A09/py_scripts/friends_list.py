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
from numba import njit
from timeit import default_timer as timer

def build_dict():
    '''
    Read in data in csv format. From this data, build a dictionary with
    all users and their information contained within. 
    '''

    # Open the input file
    input = open('user_data.csv', 'r')

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
    for i in range(0, len(user_dict)):
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
    for i in range(0, len(user_dict)):
        i = str(i)
        user_dict[i]['f_left'] = max_friends_list[int(i)]
        user_dict[i]['friends'] = set()
        user_dict[i]['max'] = max_friends_list[int(i)]
        user_dict[i]['fails'] = 0

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

    The algorithm usually runs in 5.75 minutes for 1,000,000 users.
    '''
    print("Starting friend finder...")
    start = timer()
    for user in range(0, len(users)):
        fails = 0
        user = str(user)
        # Loops until user hits friend quota or fails too many times
        while (users[user]['f_left'] > 0 and fails < tries):
            # Get index of potential friend
            # len(users) - 1 * random.random() is used instead of 
            # random.ranint(0,len(users)-1) because it is much faster
            potential = int((len(users) - 1) * random.random())
            potential = str(potential)
            if(users[potential]['f_left'] > 0):
                # Add both users to each other's friends list
                users[user]['friends'].add(potential)
                users[potential]['friends'].add(user)
                # Decrement friends left list
                users[user]['f_left'] -= 1
                users[potential]['f_left'] -= 1
            else:
                fails += 1
        users[user]['fails'] = fails

    end = timer()
    elapsed = end - start
    print(f"Matched friends for {elapsed} seconds.")

def random_make_friends(users, fails=1000, flex=0.05):
    '''
    This is the make_friends algorithm with a twist for testing purposes.
    Rather than looping through the dictionary of users in order
    from 0 to len(users) - 1 trying to find random friends, we will choose
    a random user to find a random friend. This new algorithm is an attempt
    to avoid the slow-down that comes at the end of the loop when most users
    toward the front of the dictionary have met their friend quota while 
    the users at the end have a disporportionately low friend count.

    The flex argument allows us to accept a number of friend connections
    less than the ideal number to avoid the high cost of making those final
    few friend connections.
    '''
    print("Starting test friend-finding algorithm...")
    start = timer()

    friends_made = 0
    total_friend_quota = 0
    len_users = len(users)

    # Loop through the dictionary to see the total number of connections needed
    # TODO: sum total friends needed in the allot_quota function
    for i in range(0, len(users)):
        total_friend_quota += users[str(i)]['max']

    quota = total_friend_quota - (total_friend_quota * flex)
    while(friends_made < quota):
        # Pick a random user
        rand_user = int(len_users * random.random())
        rand_user = str(rand_user)
        if (users[rand_user]['f_left'] > 0 and users[rand_user]['fails'] < fails):
            # Find a potential friend to connect with
            rand_potential = int(len_users * random.random())
            rand_potential = str(rand_potential)
            if (users[rand_potential]['f_left'] > 0 and rand_potential not in users[rand_user]['friends']):
                # Add each other as friends
                users[rand_user]['friends'].append(rand_potential)
                users[rand_potential]['friends'].append(rand_user)
                # Decrement f_left
                users[rand_user]['f_left'] -= 1
                users[rand_potential]['f_left'] -= 1
                friends_made += 1
            else:
                users[rand_user]['fails'] += 1

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
    print("Starting friend-making algorithm effectiveness test...")
    for user in range(0, len(users)):
        user = str(user)
        expected_sum += users[user]['max']
        actual_sum += len(users[user]['friends'])
    
    expected_average = expected_sum / (len(users))
    actual_average = actual_sum / (len(users))

    print(f"Average expected friend count: {expected_average}")
    print(f"Actual average friend count: {actual_average}")

def fail_stats(users, zeros=True, max=1000):
    '''
    A function for getting failure rate statistics for the friend-finding algorithm.
    Statistics include total failures as well as failures per user.

    If zeros=False, users who failed 0 times during match-making will not be shown.
    The max argument corresponds to the maximum number of tries a user can make
    in the process of meeting their friend quota.
    '''
    total_fails = 0
    max_fail_count = 0
    print("Grabbing failure statistics...")
    for i in range(0, len(users)):
        i = str(i)
        total_fails += users[i]['fails']
        if (users[i]['fails'] == max):
            max_fail_count += 1
        if(zeros):
            print(f"Fails for user{i}: {users[i]['fails']}")
        else:
            if(users[i]['fails'] == 0):
                pass
            else:
                print(f"Fails for user{i}: {users[i]['fails']}")
    print(f"Total users: {len(users)}")
    print(f"Total fails: {total_fails}")
    print(f"Total users who failed {max} times: {max_fail_count}")

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
    print("Building messages...")
    start = timer()
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

    end = timer()
    elapsed = end - start
    print(f"Generated {num_mess} in {elapsed} seconds.")

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
    

def redis_plain_users(users):
    '''
    Prints plain-text redis commands for inserting the user data generated
    in this script into a redis instance using HMSET. The friends list is created
    in a separate file and uses redis sets.

    User information: email, username, first_name, last_name, 
    password, create_time, last_update, age
    The user category information is hardcoded to avoid making too many 
    lines in the text file.
    '''

    print("Creating plain-text redis commands for inserting users and friends lists...")
    u = open('redis_users.txt', 'w')
    fr = open('redis_friends.txt', 'w')

    start = timer()
    for i in range(len(users) - 1):
        i = str(i)
        u.write("HMSET user{} email {} username {} first_name {} last_name {} password {} create_time {} last_update {} age {}\n".format(
            i, users[i]['email'], users[i]['username'], users[i]['first_name'], users[i]['last_name'],
            users[i]['password'], users[i]['create_time'], users[i]['last_update'], users[i]['age']))
        for j in range(len(users[i]['friends'])):
            fr.write("SADD friends{} {}\n".format(i, users[i]['friends'][j]))
    end = timer()
    elapsed = end - start
    print(f"Finished generating user and friend commands for redis in {elapsed} seconds.")

    u.close()
    fr.close()

def redis_plain_messages(messages):
    '''
    Prints plain-text redis commands for inserting the message data generated
    in this script into a redis instance using HMSET.
    '''
    commands = 0
    print("Creating plain-text redis commands for inserting messages...")
    f = open('redis_messages.txt', 'w')
    start = timer()
    for i in range(len(messages)):
        i = str(i)
        f.write("HMSET message{} send \"{}\" rec \"{}\" message \"{}\"\n".format(i, messages['message'+i]['send'], messages['message'+i]['rec'], messages['message'+i]['message']))
        commands += 1

    end = timer()
    elapsed = end - start
    f.close()

    print(f"Created {commands} commands in {elapsed} seconds.")


if __name__ == '__main__':
    messages = {}
    user_list = {}
    ranges = [[3,10],[11,25],[26,100],[101,250]]

    # Build user list from csv data
    user_list = build_dict()
    # Give each user a maximum number of potential friends
    allot_quota(user_list, ranges)
    # Build a list of friends for each user
    make_friends(user_list)
    #fail_stats(user_list, False)
    make_friends_test(user_list)

    
    '''
    # Create simulated message traffic
    text_model = make_model()
    build_messages(text_model, messages, user_list)

    # Test plain-text redis command generator
    redis_plain_messages(messages)
    redis_plain_users(user_list)
    '''