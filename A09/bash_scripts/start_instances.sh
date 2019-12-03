#!/bin/sh

#***********************************************************************
#
#
#
#
#***********************************************************************

# Make redis directory
mkdir redis_cluster_instance
cd redis_cluster_instance

begin=""
end=""

# Make sure a port or range of ports is specified
if [ ! $1 ]
then
	echo "Specify a port or range of ports as arguments."
	echo "Usage: <script_name> <begin_port> <end_port>"
	echo "Example: ./redis_server_start.sh 7000 7005"
	exit
fi

# Assign beginning port
begin=$1

# If no second argument exists, use $1 as begin and end port
if [ ! $2 ]
then
	end=$1	
else
	end=$2
fi

# Specify range of ports to create redis instances for
# These will be the first two arguments to the script
ports=$(seq ${begin} ${end})
startup_ports=""

# Make all config files and start each instance
for port in ${ports}
do
	startup_ports="${startup_ports}127.0.0.1:${port} "
	mkdir ${port}
	cd ${port}
	cat >redis.conf << EOF

port ${port}
cluster-enabled yes
cluster-config-file nodes.conf
cluster-node-timeout 5000
appendonly yes
protected-mode no

dir ./
loglevel notice
logfile ${port}.log

save 900 1
save 300 10
save 60 10000
EOF
	echo "Starting ${port}..."
	redis-server ./redis.conf &
	sleep 1
	cd ..
done



