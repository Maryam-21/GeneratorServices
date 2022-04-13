# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import numpy as np
import pandas as pd
import os
import re
import string
import nltk
nltk.download('punkt')
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import random

file_path = "req.txt"


def read_file(file_path):
    txt = []
    my_file = open(file_path, "r")
    txt = my_file.readlines()
    return txt

req = read_file(file_path)
print("number of lines = ", len(req))


def clean_txt(txt):
    cleaned_txt = []
    for line in txt:
        line = line.lower()
        line = re.sub(r"[,.\"\'!@#$%^&*(){}?/;`~:<>+=-\\]", "", line)
        tokens = word_tokenize(line)
        words = [word for word in tokens if word.isalpha()]
        cleaned_txt += words
    return cleaned_txt


cleaned_req = clean_txt(req)
print("number of words = ", len(cleaned_req))


def make_markov_model(cleaned_stories, n_gram=2):
    markov_model = {}
    for i in range(len(cleaned_stories) - n_gram - 1):
        curr_state, next_state = "", ""
        for j in range(n_gram):
            curr_state += cleaned_stories[i + j] + " "
            next_state += cleaned_stories[i + j + n_gram] + " "
        curr_state = curr_state[:-1]
        next_state = next_state[:-1]
        if curr_state not in markov_model:
            markov_model[curr_state] = {}
            markov_model[curr_state][next_state] = 1
        else:
            if next_state in markov_model[curr_state]:
                markov_model[curr_state][next_state] += 1
            else:
                markov_model[curr_state][next_state] = 1

    # calculating transition probabilities
    for curr_state, transition in markov_model.items():
        total = sum(transition.values())
        for state, count in transition.items():
            markov_model[curr_state][state] = count / total

    return markov_model


markov_model = make_markov_model(cleaned_req)
print("number of states = ", len(markov_model.keys()))

print("All possible transitions from 'product shall' state: \n")
print(markov_model['product shall'])


def generate_req(markov_model, limit=100, start='the'):
    n = 0
    curr_state = start
    next_state = None
    reqs = ""
    reqs += curr_state + " "
    while n < limit:
        next_state = random.choices(list(markov_model[curr_state].keys()),
                                    list(markov_model[curr_state].values()))

        curr_state = next_state[0]
        reqs += curr_state + " "
        n += 1
    return reqs

#for i in range(20):
 #   print(str(i)+". ", generate_req(markov_model, start="product shall", limit=12))


meet="The product shall interface with the Choice Parts System.  This provides the feed of recycled parts data.The product shall run on the existing hardware for all environments the product shall adhere to the corporate Architecture guidelines The product shall comply with corporate User Interface Guidelines The product shall comply with corporate color scheme The appearance of the product shall appear professional The software product is expected to run on Windows or Linux platforms. The product shall be easy to use by Adjusters and Collision Estimators.  95% of Adjusters and Collision Estimators shall find the product easy to use. The product shall increase productivity of Collision Estimators. 80% of the Collision Estimators shall agree their productivity has increase within 1 month of using the product. Users shall feel satisfied using the product.  85% of all users will be satisfied with the product. The product shall be easy to learn by Adjusters and Collision Estimators.  The product shall be learned with two days onsite training The user shall easily locate instructions while using the product.  User help can be found within 90% of the system."


def red(req,seed,l):
    req_arr=[]
    cm = clean_txt(read_file(file_path))
    print('clean text: ',cm)
    mm = make_markov_model(cm)
    print('model: ',mm)
    for i in range(20):
        req_arr.append(generate_req(mm, start=seed, limit=l))
    return req_arr


arr=red(meet,seed="product shall",l=12)
for i in range(10):
    print(arr[i])

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
