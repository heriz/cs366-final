import sys
import random
import jumble as j
from random import choice

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

def generate_email(greeting_file, body_file, closing_file, output_file):

    with open(greeting_file, "rt", encoding="utf-8") as f:
        greeting_text = f.read()
    with open(body_file, "rt", encoding="utf-8") as g:
        body_text = g.read()
    with open(closing_file, "rt", encoding="utf-8") as h:
        closing_text = h.read()

    output = open(output_file, "w")

    # remove residual empty strings
    greeting_list = list(filter(None, greeting_text.split("\n")))
    closing_list = list(filter(None, closing_text.split("\n")))

    # * is designated newline character in source text file
    for i in range(len(closing_list)):
        closing_list[i] = closing_list[i].replace('*','\n')

    greeting_words = greeting_text.split()
    greeting = build_dict(greeting_words)

    body_words = body_text.split()
    body = build_dict(body_words)

    body_EOS = ['.', '?', '!']
    
    greeting = str(random.choice(greeting_list))
    closing = str(random.choice(closing_list))

    message = ""
    body_len = random.randint(2, 4)
    paragraph_len = random.randint(1, 4)

    message += "\n" + greeting + "\n\n"

    highlighting = False

    for i in range(body_len):
        if(paragraph_len >= 0):
            paragraph_len -= 1
        else:
            message += "\n\n"
            paragraph_len = random.randint(2, 4)

        sentence = generate_sentence(body, body_EOS) + " "
        
        for word in sentence.split():
            if(j.is_replaceable_noun(word) and
               random.randint(1,100) <= j.noun_replacement_prob):
                if(highlighting):
                    message += "*" + j.switch_noun(word) + "*" + " "
                else:
                    message += j.switch_noun(word) + " "
            elif(word in j.adverb_list and
                    random.randint(1,100) <= j.adverb_replacement_prob):
                    if(highlighting):
                        message += "*" + j.switch_by_pos(word, j.adverb_list) + "*" + " "
                    else:
                        message += j.switch_by_pos(word, j.adverb_list) + " "

            elif(word in j.adjective_list and
                    random.randint(1,100) <= j.adjective_replacement_prob):
                    if(highlighting):
                        message += "*" + j.switch_by_pos(word, j.adjective_list) + "*" + " "
                    else:
                        message += j.switch_by_pos(word, j.adjective_list) + " "
            else:
                message += " " + word + " "
                
    message += "\n\n\n" + closing + "\n"

    output.write(message)

def main():
    generate_email(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])

if __name__ == "__main__":
    main()
