#!/bin/bash


#automate the running of the python script to get newly cleaned files
#will automatically set the current working directory to the current directory
FILES=`ls ./cleaned`
CWD=`pwd`

for item in $FILES
do
    #echo "python3 tag_dict.py ./cleaned/$item data.yaml"
    `python3 $CWD/tag_dict.py $CWD/cleaned/$item $CWD/data.yaml`
done
