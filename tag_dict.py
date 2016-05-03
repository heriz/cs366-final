import os, sys
import yaml
from collections import defaultdict

"""
    to run this code:
    python3 tag_dict.py [name of file which is output from msg_cleaner.py or
    text_file_to_tagged.py] [yaml file which you want to use to store data]

    [] indicate a filename parameter in the form *.* because it doesn't really
    matter to a computer. :)

"""

def main(arg):
  input_file = arg[1]
  yaml_file = arg[2]
  #do this so that way there are empty lists for empty entries
  all_tags = defaultdict(list)
  #pretty print statement to make the script more friendly
  print("Adding terms and tags for " + input_file + " to " + yaml_file + "!")
  ark_output = open(input_file, "r")
  for lines in ark_output:
    #print(lines)
    lines = lines.strip()
    word_pairs = lines.split(" ")
    #default dict lets me like, make things nicer
    for pairs in word_pairs:
      #print(pairs)
      #some of the tag pairs are messed up, ignore that messed up-ness
      word, tag = pairs.split("_")[:2]
      all_tags[tag].append(word)
     
  if os.path.exists(yaml_file):
    #do some stuff to get the current values of the yaml written to hard disk
    temp = defaultdict(list)
    read_file = open(yaml_file, "r")
    tags = yaml.load(read_file)
    #hahahaha... this is ridiculous
    for entries in tags:
      #do a merge of the two lists
      temp[entries] = tags[entries] + all_tags[entries]
      #get rid of all the duplicates
      temp[entries] = list(set(temp[entries]))
    #close this file
    read_file.close()
    #so you can remove it
    os.remove(yaml_file)
    #output this new temporary dictionary into the same yaml name
    output = open(yaml_file,"w")
    yaml.dump(temp, output)
    output.close()
  else:
    output = open(yaml_file, "w")
    for entries in all_tags:
      all_tags[entries] = list(set(all_tags[entries]))
    yaml.dump(all_tags, output)
    output.close()


if __name__ == "__main__":
  main(sys.argv)
