import random
import yaml
from collections import defaultdict
from yaml.representer import Representer
from nltk.corpus import wordnet as wn

with open("data.yaml", 'r') as f:
    try:
        tag_data = yaml.load(f.read())
    except yaml.YAMLError as exc:
        print(exc)

noun_list = tag_data["NN"]
adjective_list = tag_data["JJ"]
adverb_list = tag_data["RB"]

noun_replacement_prob = 30 # percent
adjective_replacement_prob = 40 # percent
adverb_replacement_prob = 20 # percent

def is_replaceable_noun(word):
    if(len(wn.synsets(word)) > 0 and
       len(wn.synsets(word)[0].hypernyms()) > 0 and
       word in noun_list):
        return True
    else:
        return False

def switch_noun(word):
    word = wn.synsets(word)[0]
    parent = word.hypernyms()[0]
    substitute = random.choice(parent.hyponyms())
    substitute_word = substitute.name()
    new_noun = wn.synset(substitute_word).name().split('.')[0].replace('_', ' ')
    return new_noun
    
def switch_by_pos(word, pos_list):
    new_word = random.choice(pos_list)
    # non-nouns should be standard English
    if(len(wn.synsets(new_word)) > 0):
        return new_word
    else:
        return word
