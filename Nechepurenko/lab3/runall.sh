#!/bin/sh
for t in Tests/*;
do 
	echo "Input:"
	cat $t;
	echo "\n\nOutput:"
	python3 Source/lab3.py < $t ;
	echo "\n\n" 
done
