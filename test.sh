#!/bin/bash
exec 3>&1 4>&2
trap 'exec 2>&4 1>&3' 0 1 2 3
exec 1>test.log 2>&1
for i in {1..50}
do
	printf "Execution %s of 50" "$i"
	python3 -m instagram.testing.basic_test
	echo "waiting 3 seconds"
	sleep 3
done

