#!/usr/bin/python

import sys

DELEM = sys.argv[1]
INPUT = {}
i = 0

for line in sys.stdin:
	INPUT[i]=line
	i = i+1

	
newList = []
for i in range(len(INPUT)):
	l = []
	l = INPUT[i].strip().split(DELEM)
	string = l[len(l)-1]
	for j in range(len(l)-2,-1, -1):
		string = string + DELEM + l[j]
	print(string)
