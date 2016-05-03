import os, sys
import yaml
from collections import defaultdict

def main(arg):
  input_file = arg[1]
  yaml_file = arg[2]
  all_tags = defaultdict(list)
  print("Adding terms and tags for " + input_file + " to " + yaml_file + "!")
  ark_output = open(input_file, "r")
  for lines in ark_output:
    #print(lines)
    lines = lines.strip()
    word_pairs = lines.split(" ")
    #default dict lets me like, make things nicer
    for pairs in word_pairs:
      #print(pairs)
      word, tag = pairs.split("_")[:2]
      all_tags[tag].append(word)
     
  #for entries in all_tags.keys():
  #  print(entries)

  if os.path.exists(yaml_file):
    temp = defaultdict(list)
    read_file = open(yaml_file, "r")
    tags = yaml.load(read_file)
    for entries in tags:
      temp[entries] = tags[entries] + all_tags[entries]
      temp[entries] = list(set(temp[entries]))
    read_file.close()
    os.remove(yaml_file)
    output = open(yaml_file,"w")
    yaml.dump(temp, output)
    output.close()
    #everytag = merge(tags, all_tags)
    #yaml.dump(everytag, output)
  else:
    output = open(yaml_file, "w")
    yaml.dump(all_tags, output)
    output.close()


if __name__ == "__main__":
  main(sys.argv)
