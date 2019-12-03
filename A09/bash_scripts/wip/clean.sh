#!/bin/sh

# Flush all nodes
ports=$(seq $1 $2)

for port in ${ports}
do
	redis-cli -c -p ${port}
	expect "127.0.0.1:${port}>"
	send "flushall"
	expect "127.0.0.1:${port}>"
	send "cluster reset"
	expect "127.0.0.1:${port}>"
	send "exit"
done

pkill redis-server
rm -rf redis_cluster_instance
