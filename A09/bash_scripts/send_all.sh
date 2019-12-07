#!/bin/sh

#****************************************************
# A quick and dirty script for sending files to
# the other computers in BO120. This script assumes
# it is being run in the same folder as the file you
# wish to send.
#
# Usage: ./send_all.sh some_file.txt
#****************************************************

ips=("88.173" "89.7" "88.228" "89.9" "88.237" "88.157" "88.255" "88.245" "89.8" "88.205" "88.241")

for ip in ${ips[@]}
do
	 scp $1 student@10.0.${ip}:/Users/student/Desktop
done


