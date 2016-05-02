import sys
import random
from random import choice
from pprint import pprint

EOS = ['.', '?', '!']

numlist = list(range(30))

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
        #
        d[key].append(third)

    return d

def generate_sentence(d):
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
        if third[-1] in EOS:
            break
        # else
        key = (second, third)
        first, second = key
 
    return ' '.join(li)

def main():
    fname = sys.argv[1]
    with open(fname, "rt", encoding="utf-8") as f:
        text = f.read()

    words = text.split()
    d = build_dict(words)
    #pprint(d)
    print()
    for i in range(random.randint(15, 25)):
        sent = generate_sentence(d)
        print(sent)

main()
