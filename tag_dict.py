import os, sys
import yaml
from collections import defaultdict

def merge_two_dicts(x, y):
  z = x.copy()
  z.update(y)
  return z

def main(arg):
  input_file = arg[1]
  yaml_file = arg[2]
  all_tags = defaultdict(list)
  ark_output = open(input_file, "r")
  for lines in ark_output:
    lines = lines.strip()
    word_pairs = lines.split(" ")
    #default dict lets me like, make things nicer
    for pairs in word_pairs:
      word, tag = pairs.split("_")
      all_tags[tag].append(word)
     
  #for entries in all_tags.keys():
  #  print(entries)

  if os.path.exists(yaml_file):
    output = open(yaml_file, "r")
    tags = yaml.load(output)
    print(tags)
    #everytag = merge_two_dicts(tags, all_tags)
    #yaml.dump(everytag, output)
  #else:
    output = open(yaml_file, "w")
    yaml.dump(all_tags, output)

  output.close()


if __name__ == "__main__":
  main(sys.argv)
