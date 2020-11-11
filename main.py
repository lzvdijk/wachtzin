""" 
Pseudorandom passphrase generator in Dutch.

Wordlist originally created by: https://github.com/OpenTaal/opentaal-wordlist 

Curated down to 144336 words by removing overly long words, words containing 
special characters and potentially offensive phrases (don't judge I need to send these to customers)
"""

import secrets
import markovify
import spacy

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


def generate(length):
    """generate a passphrase of $length words"""
    passphrase = []
    for i in range(length):
        passphrase.append(randomword())
    return passphrase


def get_password_length():
    input_chosen = False
    while input_chosen == False:
        print("Enter your desired passphrase length:")
        length = input()
        try:
            length = int(length)
            input_chosen = True
            global cyberveiligheid
            global cybercorpus
            if length == 1337 and cybercorpus == True:
                print("Engaging cyberveiligheidsmatrix!")
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

# setup wordlist/corpus
try:
    rian = open('./source.txt', encoding='utf8').read()
    aivd = open('./sources/combined_aivd_reports.txt', encoding='utf8').read()
    text_model_a = POSifiedText(rian, state_size=3)
    # text_model_b = POSifiedText(aivd, well_formed = False, state_size=3)
    # text_model = markovify.combine([text_model_a, text_model_b ], [ 3, 1 ])
    cybercorpus = True
except Exception as e:
    print("Error loading text source")

words = open('wordlist-easy.txt', encoding='utf8').read().splitlines()


# setup user vars
length = get_password_length()
count = get_password_count()

# generate and print
if cyberveiligheid:    
    for i in range(count):
        sentence = None
        while sentence is None: # model might error out and return a None object, just retry generation
            sentence = text_model_a.make_short_sentence(100)
            if sentence and len(sentence)< 20: # disregard short sentences
                sentence = None
        sentence = strip_sentence(sentence)
        print(sentence)
else:
    for i in range(count):
        sentence = ' '.join(generate(length))
        print(sentence.replace("\n", ""))