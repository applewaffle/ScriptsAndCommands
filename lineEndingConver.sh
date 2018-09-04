#!/bin/bash

# This script converts a file whtat has charage retruns for line ending to one whith only
# '\n' (newlines) as the line endings.

if [ -e tempNewFile.txt ]; then
   rm tempNewFile.txt
fi

if [ $# -ne 1 ]; then
   echo "Usage: ${0##*/} file.txt"
   exit
fi

tr -d '\r' < $1 > tempNewFile.txt
cat tempNewFile.txt > $1
rm tempNewFile.txt
