##!/usr/bin/env python

#****************************************************************************
# A simple script for building a list of friends for a redis cluster.
#
# Usage: ./build_friends.py 
#****************************************************************************

from timeit import default_timer as timer

# Open the input file
input = open("data.csv", 'r')

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
