#!/usr/bin/env python

from rediscluster import RedisCluster

# Start
startup_nodes = [{"host": "127.0.0.1", "port": "7000"}]

rc = RedisCluster(startup_nodes=startup_nodes, decode_responses=True)

# Test the connection
if(rc.ping()):
    print("Connection successful...")


print(rc.hmset("user:0", {"name": "person", "age": 90}))


