#!/bin/sh
for t in Tests/1/*;
do 
	echo "Input:"
	cat $t;
	echo "Output:"
	python3 Source/lab5.py < $t ;
done
for t in Tests/2/*;
do 
	echo "Input:"
	cat $t;
	echo "Output:"
	python3 Source/stepik5_2.py < $t ;
done