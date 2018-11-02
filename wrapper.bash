#!/bin/bash

executable_script=$1
incident=$2
issue=$3

qa_test=$(node $executable_script lint) > output.txt

echo $(cat output.txt)
echo $qa_test


which python

if [[ qa_test != 0 ]]
then
	/usr/bin/python python create_alert.py -a $incident $issue
else
	echo "tests passed"
fi