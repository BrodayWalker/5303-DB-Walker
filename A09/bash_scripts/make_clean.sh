#!/bin/sh

# This kills the cluster in a not-so-graceful way
pkill redis-server

# Remove all cluster instance files
rm -rf redis_cluster_instance
