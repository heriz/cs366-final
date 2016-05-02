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
    greeting_file = sys.argv[1]
    body_file = sys.argv[2]
    closing_file = sys.argv[3]
    
    with open(greeting_file, "rt", encoding="utf-8") as f:
        greeting_text = f.read()
    with open(body_file, "rt", encoding="utf-8") as g:
        body_text = g.read()
    with open(closing_file, "rt", encoding="utf-8") as h:
        closing_text = h.read()

    greeting_words = greeting_text.split()
    greeting = build_dict(greeting_words)

    body_words = body_text.split()
    body = build_dict(body_words)

    closing_words = closing_text.split()
    closing = build_dict(closing_words)
    
    #pprint(d)
    print("\n" + generate_sentence(greeting) + "\n")
    for i in range(random.randint(3, 12)):
        print(generate_sentence(body))
    print("\n" + generate_sentence(closing) + "\n")


main()
