# usage:
# python3 markov.py [greeting text file] [body text file] [closing text file]
#
# example:
# python3 markov.py greetings-cappy.txt cappy.mbox.txt closings-cappy.txt

import sys
import random
from random import choice
from pprint import pprint

body_EOS = ['.', '?', '!']
greeting_EOS = [',', '.', '!', ':']

numlist = list(range(30))

body_len = random.randint(3, 12)

def build_dict(words):
    """
    Build a dictionary from the words.

    (word1, word2) => [w1, w2, ...]  # key: tuple; value: list
    """
    d = {}
    for i, word in enumerate(words):
        try:
            first, second, third = words[i], words[i+1], words[i+2]
        except IndexError:
            break
        key = (first, second)
        if key not in d:
            d[key] = []
        d[key].append(third)

    return d

def generate_sentence(d, eos):
    li = [key for key in d.keys() if key[0][0].isupper()]
    key = choice(li)

    li = []
    first, second = key
    li.append(first)
    li.append(second)
    while True:
        try:
            third = choice(d[key])
        except KeyError:
            break
        li.append(third)
        if third[-1] in eos:
            break
        # else
        key = (second, third)
        first, second = key
 
    return ' '.join(li)

def main():
    greeting_file = sys.argv[1]
    body_file = sys.argv[2]
    closing_file = sys.argv[3]
    
    with open(greeting_file, "rt", encoding="utf-8") as f:
        greeting_text = f.read()
    with open(body_file, "rt", encoding="utf-8") as g:
        body_text = g.read()
    with open(closing_file, "rt", encoding="utf-8") as h:
        closing_text = h.read()

    # remove residual empty strings
    closing_list = list(filter(None, closing_text.split("\n")))

    # * is designated newline character in source text file
    for i in range(len(closing_list)):
        closing_list[i] = closing_list[i].replace('*','\n')
    
    greeting_words = greeting_text.split()
    greeting = build_dict(greeting_words)

    body_words = body_text.split()
    body = build_dict(body_words)

    greeting = generate_sentence(greeting, greeting_EOS)
    closing = str(random.choice(closing_list))
    
    print("\n" + greeting + "\n")
    for i in range(body_len):
        print(generate_sentence(body, body_EOS))
    print("\n" + closing + "\n")


main()
