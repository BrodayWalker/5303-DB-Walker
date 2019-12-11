#!/usr/bin/env python3

import json
import sys
import random
import io
import markovify

def build_messages(messages, f='messages.json'):
    f = open(f, 'r')

    f_data = f.read()
    #f_data = json.loads(f_str)

    print(type(f_data))
    print(len(f_data))
    print(f_data[0])
    print(f_data[1])

    # Grab a random message
    rando = int((len(f_data) - 1) * random.random())
    print(f_data[rando])

    # Assign to a dictionary
    for i in range(0, len(f_data), 2):
        messages[str(f_data[i])] = str(f_data[i+1])

    

    f.close()

def gen_messages(text_model, messages):
    pass
    
if __name__ == '__main__':
    messages = {}

    # Train the model
    infile = 'conversations.txt'
    with io.open(infile, 'r', encoding='utf-8') as f:
        text = f.read()

    text_model = markovify.Text(text)

    print(text_model.make_sentence())



    #build_messages(messages)