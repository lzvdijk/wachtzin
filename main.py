""" 
Pseudorandom passphrase generator in Dutch.

Wordlist originally created by: https://github.com/OpenTaal/opentaal-wordlist 

Curated down to 144336 words by removing overly long words, words containing 
special characters and potentially offensive phrases (don't judge I need to send these to customers)
"""

import secrets
import markovify
import spacy
import re

nlp = spacy.load("nl_core_news_sm")

cybercorpus = False
cyberveiligheid = False

class POSifiedText(markovify.Text):
    def word_split(self, sentence):
        return ["::".join((word.orth_, word.pos_)) for word in nlp(sentence)]

    def word_join(self, words):
        sentence = " ".join(word.split("::")[0] for word in words)
        return sentence


def randomword():
    try:
        word = secrets.choice(words)
        return(word)
    except Exception as e:
        return(f"Error generating word! {e}")
        

def generate(count, length):
    """generate a passphrase of $length words"""
    for i in range(count):
        passphrase = []
        for o in range(length):
            passphrase.append(randomword())
        sentence = ' '.join(passphrase)
        sentence = reg_strip_sentence(sentence)
        print(sentence)


def get_password_length():
    input_chosen = False
    while input_chosen == False:
        print("Enter your desired passphrase length:")
        length = input()
        try:
            length = int(length)
            input_chosen = True
            global cyberveiligheid
            if length == 1337:
                print("Engaging cyberveiligheidsmatrix! This will take a while!")
                cyberveiligheid = True        
        except Exception as e:
            print(f"Invalid input! {e}")
    return length


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


def strip_sentence(sentence):
    try:
        sentence = sentence.replace("\n", "")
        sentence = sentence.replace("  ", " ")
        sentence = sentence.replace(" , ", ", ")
        sentence = sentence.replace(" ' ", "'")
        sentence = sentence.replace(" . ", ". ")
        sentence = sentence.replace(" .", ".")
        sentence = sentence.replace("( ", "(")
        sentence = sentence.replace(" )", ")")
        sentence = sentence.replace(" ’ ", "'")
        sentence = sentence.replace(" : ", ": ")
        sentence = sentence.replace(" ; ", "; ")
    except Exception as e:
        pass
    return sentence


def reg_strip_sentence(sentence):
    sentence = re.sub('[^A-Za-z0-9 ]+', '', str(sentence))
    sentence = re.sub('[  ]+', ' ', str(sentence))
    return sentence

def setup_corpus():
# setup wordlist/corpus
    try:
        # source1 = open('./sources/marsman.txt', encoding='utf8').read()
        # text_model = POSifiedText(source1, state_size=2)

        source1 = open('./sources/marsman.txt', encoding='utf8').read()
        source2 = open('./sources/vangeel.txt', encoding='utf8').read()
        source3 = open('./sources/nijhof.txt', encoding='utf8').read()
        text_model_a = POSifiedText(source1, state_size=2)
        text_model_b = POSifiedText(source2, state_size=2)
        text_model_c = POSifiedText(source3, state_size=2)
        text_model = markovify.combine([text_model_a, text_model_b, text_model_c ], [ 1, 1, 1 ])

        # source1 = open('./sources/combined_aivd_reports.txt', encoding='utf8').read()
        # source2 = open('./sources/security.nl.txt', encoding='utf8').read()
        # source3 = open('./source.txt', encoding='utf8').read()
        # text_model_a = POSifiedText(source1, state_size=3)
        # text_model_b = POSifiedText(source2, state_size=3)
        # text_model_c = POSifiedText(source3, state_size=3)
        # text_model = markovify.combine([text_model_a, text_model_b, text_model_c ], [ 1, 1, 1 ])
        return text_model
    except Exception as e:
        print(f"Error loading text source: {e}")


def do_generation():
    # setup user vars
    length = get_password_length()
    count = get_password_count()

    # generate and print
    if cyberveiligheid:
        try:
            text_model = setup_corpus()
            for i in range(count):
                sentence = None
                while sentence is None: # model might error out and return a None object, just retry generation
                    sentence = text_model.make_short_sentence(80)
                    if sentence and len(sentence)< 30: # disregard short sentences
                        sentence = None
                sentence = reg_strip_sentence(sentence)
                sentence = str.lower(sentence)
                print(sentence) 
            return None
        except Exception as e:
            pass

    else:
        generate(count, length)

words = open('wordlist-easy.txt', encoding='utf8').read().splitlines()
do_generation()