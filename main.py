""" 
Pseudorandom passphrase generator in Dutch.

Wordlist originally created by: https://github.com/OpenTaal/opentaal-wordlist 

Curated down to 144336 words by removing overly long words, words containing 
special characters and potentially offensive phrases (don't judge I need to send these to customers)
"""

import secrets

# prepare wordlist
words = open('wordlist-easy.txt').read().splitlines()

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


# setup user vars
length = get_password_length()
count = get_password_count()

# generate and print
for i in range(count):
    print(' '.join(generate(length)))