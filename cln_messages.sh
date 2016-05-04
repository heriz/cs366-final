#!/bin/bash


#automate the running of the python script to get newly cleaned files
#will automatically set the current working directory to the current directory
FILES=`ls *.mbox`
CWD=`pwd`

#for item in $FILES
#do
#    #IFS=. elem=($item)
#    textfile="${item[0]}.txt"
#    `mkdir cleaned`
#    echo "python3 $CWD/msg_cleaner.py $CWD/$item $CWD/cleaned/$textfile"
#    `python3 $CWD/msg_cleaner.py $CWD/$item $CWD/cleaned/$textfile`
#done

for item in $FILES
do
    #IFS=. elem=($item)
    textfile="${item[0]}.txt"
    `mkdir cleaned_tag_only`
    echo "python3 $CWD/msg_cleaner.py $CWD/$item $CWD/cleaned_tag_only/$textfile t t"
    `python3 $CWD/msg_cleaner.py $CWD/$item $CWD/cleaned_tag_only/$textfile t t`
done
