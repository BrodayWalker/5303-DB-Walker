#############################################################################
#                                                                           #
#                   Broday Walker's RESP Command Generator                  #
#                                                                           #
#############################################################################

import argparse
import sys

# Create an argument parser
parser = argparse.ArgumentParser(description="A script for converting " 
    "CSV data to Redis Serial Protocol.")
# Positional Arguments
parser.add_argument("filename", help="The name of the file you wish to "
    "convert.")
# Optional Arguments
parser.add_argument("-o", "--output", dest="output", default="output.txt", 
    help="Specify the name of the output file. If no name is provided, "
    "the file will be named output.txt")
parser.add_argument("-t", "--type", dest="type", default="hash", 
    help="Specify the type of Redis data structure. Type is set to hash by "
    "default.")
parser.add_argument("--header", dest="header", default=False, 
    action="store_true",
    help="Set to true if there is a header in your CSV file." )
# Non-optional but not positional arguments
# The fields argument(s) are more easily handled as optional arguments 
# rather than positional.
parser.add_argument("--fields", dest="fields", nargs="*", 
    help="A list of field names that describe the data being processed.")

# Parse the arguments
args = parser.parse_args()

# Testing the arguments
print("Printing arguments for testing:\n{}".format(args))

# Open data file
print("Opening file: {}".format(args.filename))
data = open(args.filename, "r")
# Open output file which will contain redis commands
print("Opening output file for printing: {}".format(args.output))
out = open(args.output, "w")

if(args.header):
    # The first line of the data file contains labels. We don't want to use 
    # this in our logic. This essentially consumes the header without using 
    # it in any way.
    labels = data.readline()
    labels = labels.splitlines()[0]
    labels = labels.split(sep=",")

#############################################################################
#   The following is an example of the redis protocol which can be
# found at https://redis.io/topics/mass-insert
#
#   A command should look as follows (newlines shown for clarity):
#           *<args><cr><lf>            
#           $<len><cr><lf>
#           <arg0><cr><lf>   
#           <arg1><cr><lf>
#           ...
#           <argN><cr><lf>            
# 
#           Example:
#           $3<cr><lf>
#           SET<cr><lf>
#           $3<cr><lf>
#           key<cr><lf>
#           $5<cr><lf>
#           value<cr><lf>
#   
#############################################################################

# Each row of data will be handled on one line.
# We must know the length of the array.
# For hashes, the default type in this script, the length of the array is 
# 2 + (2 * len(fields)) because the command is HMSET <hash> <key1> <value1>
# ... <keyN> <valueN>
arr_len = 2 + (2 * len(args.fields))

f_lengths = []
# Get length of each field
for field in args.fields:
    f_lengths.append(len(field))

# May change this in the future for more flexibility. These are the last 
# items left hard-coded.
user_id = 0
command = "HMSET" # Used to set multiple hash fields

for line in data:
    line = line.splitlines()[0] # Remove trailing newline character
    line = line.split(sep=",") # Make line a list
    user_len = len("user:{}".format(user_id))
    
    # Abandon hope all ye who generate redis pipe data here. 
    
    # Print array and command length
    out.write(f"*{arr_len}\\r\\n${len(command)}\\r\\n{command}\\r\\n"
        f"${user_len}\\r\\nuser:{user_id}\\r\\n")
    # Loop through the line list and print the command
    i = 0
    for piece in line:
        out.write(f"${f_lengths[i]}\\r\\n{args.fields[i]}\\r\\n"
        f"${len(piece)}\\r\\n{piece}\\r\\n")
        i += 1
    
    user_id += 1

data.close()
out.close()
