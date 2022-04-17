# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import numpy as np
import pandas as pd
import os
import re
import string
import nltk
#nltk.download('punkt')
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import random

file_path = "req.txt"


def read_file(file_path):
    txt = []
    my_file = open(file_path, "r")
    txt = my_file.readlines()
    return txt

#req = read_file(file_path)
#print("number of lines = ", len(req))


def clean_txt(txtf):
    cleaned_txt = []
    txt = txtf.split(".")
    print(txt)
    for line in txt:
        print(line)
        line = line.lower()
        line = re.sub(r"[,.\"\'!@#$%^&*(){}?/;`~:<>+=-\\]", "", line)
        tokens = word_tokenize(line)
        words = [word for word in tokens if word.isalpha()]
        cleaned_txt += words
    return cleaned_txt


#cleaned_req = clean_txt(req)
#print("number of words = ", len(cleaned_req))


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


#markov_model = make_markov_model(cleaned_req)
#print("number of states = ", len(markov_model.keys()))

#print("All possible transitions from 'product shall' state: \n")
#print(markov_model['product shall'])


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


meet="Good Morning News. How are you doing? How are you soon? It's our first from many more meetings are fun and beneficial. Okay. Can I record the meetings? Of course? OK, Google, can you receive describe what you need to do? I want to build a weather station, open up the phone. That's the for the tcsd community. It should be a blog sites where anyone can share their thoughts and problems. They can communicate with others to sounds great. Looks like, when registering a new account the PTSD patients should avoid his username fast with phone number gender, his birthday. The year of his drama and a brief description of his case and whether he is under a doctor's supervision or not, Yes sure. It is an essential Parts. They can also log in as guests to navigate, but not to participate in anything. Yes. He can. He just can't write a comment or enter a room. What do you mean by that? The luggage in users can enter a room based on their gender or age? Is he wants, what does a room the first from a Blog? A room? It's a private face. To people feel more free to share their thoughts. The rooms Edmonds, is the creator of the room. He can invite the admin can make their own private or public. What's the difference between a private room and the public one? A public room will be visible. So that users can request to enter the room while a private one. No one will know our room exists except that users in the room. Can I guess tentaroo know? Okay, how can a user login? Yes, a user can follow. Unfollow, hide orphan users. The application should suggest users with similar cases to login users. In order to connect a user. Can also write whatever he wants in his blog, as long as it means the applications policy. What's the address for the sea? Can we discuss it in the next meeting? I didn't finish. It says you like I can say, we can see the next meeting. Sounds good. When is it going to be? Well, maybe after 2 weeks to schedule. Perfect. Thank you. Anytime. Sorry more functionality before I forget. Yes, of course. What is it? A user can choose whether he wants to be anonymous or not. Okay, that's a pretty good feature to start within the next meeting. Yes. I thought so too. Okay. Thank you. Goodbye. See you soon. "

def red(req,seed,l):
    req_arr=[]
    cm = clean_txt(req)
    print('clean text: ',cm)
    mm = make_markov_model(cm)
    print('model: ',mm)
    for i in range(20):
        req_arr.append(generate_req(mm, start=seed, limit=l))
    return req_arr

#arr=red(meet,seed="user can",l=10)
#for i in range(5):
    #print(arr[i])

arr=red(meet,seed="user can",l=10)
for i in range(10):
    print(arr[i])


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

# Press the green button in the gutter to run the script.

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
