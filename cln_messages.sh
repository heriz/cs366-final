#!/bin/bash


#automate the running of the python script to get newly cleaned files
FILES=`ls *.mbox`
CWD=`pwd`

for item in $FILES
do
    #IFS=. elem=($item)
    textfile="${item[0]}.txt"
    echo "python3 $CWD/msg_cleaner.py $CWD/$item $CWD/$textfile"
    `python3 $CWD/msg_cleaner.py $CWD/$item $CWD/$textfile`
done
