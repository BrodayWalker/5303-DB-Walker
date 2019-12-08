#!/usr/bin/env python

import redis

# Connect to port 7000 of our cluster
r = redis.Redis(host='10.0.88.173', port=7000)

# Test the connection
if(r.ping()):
    print("Connection successful...")

print(r.hmset("user:0", {"name": "Broday", "age": 27}))
