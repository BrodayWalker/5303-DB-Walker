#!/bin/sh

if [ ! $1 ]
then
	echo "Please input an argument"
	exit
fi
	

x=$(seq $1 $2)

tstring=""

for port in ${x}
do
	tstring="${tstring}127.0.0.1:${port} "
done

echo $[tstring}
