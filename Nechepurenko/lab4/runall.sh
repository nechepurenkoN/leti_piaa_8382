#!/bin/sh
for t in Tests/*;
do 
	echo "Input:"
	cat $t;
	echo "Output:"
	Source/lab4 < $t;
done
