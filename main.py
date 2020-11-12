""" 
Pseudorandom passphrase generator in Dutch.

Generates poetry based on the public works of Marsman, van Geel and Nijhof
"""

import markovify
import spacy
import re

try:
    nlp = spacy.load("nl_core_news_sm")
except Exception as e:
    print("Error loading spacy model! Did you run 'python -m spacy download nl_core_news_sm' ?")


class POSifiedText(markovify.Text):
    def word_split(self, sentence):
        return ["::".join((word.orth_, word.pos_)) for word in nlp(sentence)]

    def word_join(self, words):
        sentence = " ".join(word.split("::")[0] for word in words)
        return sentence


def get_password_count():
    input_chosen = False
    while input_chosen == False:
        print("Enter your desired number of passphrases:")
        length = input()
        try:
            length = int(length)
            input_chosen = True        
        except Exception as e:
            print(f"Invalid input! {e}")
    return length


def reg_strip_sentence(sentence):
    sentence = re.sub('[^A-Za-z0-9 ]+', '', str(sentence))
    sentence = re.sub('[  ]+', ' ', str(sentence))
    return sentence


def setup_corpus():
# setup wordlist/corpus
    try:
        source1 = open('./sources/marsman.txt', encoding='utf8').read()
        source2 = open('./sources/vangeel.txt', encoding='utf8').read()
        source3 = open('./sources/nijhof.txt', encoding='utf8').read()
        text_model_a = POSifiedText(source1, state_size=2)
        text_model_b = POSifiedText(source2, state_size=2)
        text_model_c = POSifiedText(source3, state_size=2)
        text_model = markovify.combine([text_model_a, text_model_b, text_model_c ], [ 2, 2, 1 ])
        return text_model
    except Exception as e:
        print(f"Error loading text source: {e}")


def do_generation():
    # setup user vars
    count = get_password_count()

    # generate and print
    try:
        text_model = setup_corpus()
        for i in range(count):
            sentence = None
            while sentence is None: # model might error out and return a None object, just retry generation
                sentence = text_model.make_short_sentence(140)
                if sentence and len(sentence)< 60: # disregard short sentences, regenerate
                    sentence = None
            sentence = reg_strip_sentence(sentence)
            sentence = str.lower(sentence)
            print(sentence) 
        return None
    except Exception as e:
        pass

do_generation()