#!/bin/sh

keys=$(seq $1 $2)

for key in ${keys}
do
	echo "SET test:${key} ${key}"
done
