#!/bin/bash
i=0
while :
do
	d=`date +%Y-%M-%d\ %H:%M:%S`
	echo "$d loop: $i"
	/root/script/cloud2tape.py -c -q -f
	echo "Press [CTRL+C] to stop.."
	i=$((i+1))
	sleep 3600
done
