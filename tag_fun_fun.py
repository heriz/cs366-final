from collections import defaultdict
import yaml
import random
import sys, os

def replace_word_random(tag, dictionary):
  options = len(dictionary[tag])
  if options > 0:
    choice = random.randint(0, options - 1)
    return dictionary[tag][choice]
  else:
    return ""

def main(arg):
  input_file = arg[1]
  output_file = arg[2]
  yaml_file = open("data.yaml", "r")
  dict_file = yaml.load(yaml_file)
  yaml_file.close()
  lines = open(input_file, "r")
  line_list = list()
  for line in lines:
    word_list = list()
    words = line.split(" ")
    for word in words:
      word_list.append(replace_word_random(word, dict_file))
    line_list.append(" ".join(word_list))
  lines.close()
  write_file = open(output_file, "w")
  for line in line_list:
    write_file.write(line+"\n")
  write_file.close()


if __name__ == "__main__":
  main(sys.argv)
