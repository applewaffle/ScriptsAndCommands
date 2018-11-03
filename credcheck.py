#!/usr/bin/python

from sys import argv
from base64 import b64decode
import re

if len(argv) != 3:
   print(argv[0] + ' token burp-input-file')
   quit()

#
param = re.compile('%s=([^;& \x00\x0C\x0D\x0E\x0F]+)'%argv[1])
inName = argv[2]
outName = "results.txt"
request = re.compile('<request base64=\"true\"><!\[CDATA\[(.*)\]\]></request>')
response=re.compile('<response base64=\"true\"><!\[CDATA\[(.*)\]\]></response>')
inputFile = open(inName, "r")

i = 0
results = {}

for line in inputFile:
   m = request.search(line)
   if m:
      r = b64decode(m.group(1)).strip().split('\n')
      for l in r:
         print l
      for l in r:
         m = param.findall(l)
         if m:
            for s in m:
               if s not in results.keys():
                  results[s] = 1
               else:
                  results[s] += 1
            break

inputFile.close()
for j,k in results.items():
   print(j + ", " + str(k))
