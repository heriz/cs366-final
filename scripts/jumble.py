import random
from nltk.corpus import wordnet as wn

replacement_prob = 30 # percent

#def identify_noun(word):

def replace_noun(tagged_word):
    word = wn.synsets(tagged_word[:-3])[0]
    parent = word.hypernyms()[0]
    substitute = random.choice(parent.hyponyms())
    substitute_word = substitute.name()
    print(wn.synset(substitute_word).name().split('.')[0])


if(random.randint(1,100) <= replacement_prob):
    replace_noun("chicken_NN")
