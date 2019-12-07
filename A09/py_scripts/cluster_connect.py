#!/usr/bin/env python

from rediscluster import RedisCluster

# Start
startup_nodes = [{"host": "10.0.88.173", "port": "7000"}]

rc = RedisCluster(startup_nodes=startup_nodes, decode_responses=True)

# Test the connection
if(rc.ping()):
    print("Connection successful...")

# One command test
print(rc.hmset("user:0", {"name": "person", "age": 90}))

# Pipeline test
# Open pipeline
p = rc.pipeline()

p.command_stack = []

# Build commands to send
for i in range(10):
    p.command_stack.append((["SET", "user:{id}".format(id=i), "person"], {}))

# Send the commands
p.execute()





