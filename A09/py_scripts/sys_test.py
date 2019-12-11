#!/usr/bin/env python3

import os
import sys
import subprocess

def redis_commands():
    filepath = 'redis_users.txt'
    sleep = "sleep 0.001"

    with open(filepath) as fp:
        for line in fp:
            line = fp.readline()
            line.rstrip("\n")
            
            cmd = "echo \"{}\" | redis-cli -c -p 7000".format(line)
            os.system(cmd)
            os.system(sleep)


if __name__ == '__main__':
    redis_commands()

    
    

