# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import numpy as np
import pandas as pd
import os
import re
import string
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import random

file_path = "req.txt"
actors = ["user", "system", "spotify", "profile", "organizer", "users"]
verbs = ["should", "could", "can", "shall", "must", "would", "will", "to", "who"]


def read_file(file_path):
    txt = []
    my_file = open(file_path, "r")
    txt = my_file.readlines()
    return txt


# req = read_file(file_path)
# print("number of lines = ", len(req))

# meeting script is taken as a parameter to preprocess it to be ready for the markov model

def clean_txt(meetingscript):
    cleaned_txt = []
    txt = meetingscript.split(".")
    # txt = meetingscript
    # print(txt)
    for line in txt:
        # print(line)
        line = line.lower()
        line = re.sub(r"[,.\"\'!@#$%^&*(){}?/;`~:<>+=-\\]", "", line)
        tokens = word_tokenize(line)
        words = [word for word in tokens if word.isalpha()]
        cleaned_txt += words
    return cleaned_txt


# cleaned_req = clean_txt(req)
# print("number of words = ", len(cleaned_req))

# the Markov model is generated by 2 n-grams "two words"
def make_markov_model(cleaned_meeting, n_gram=2):
    markov_model = {}
    for i in range(len(cleaned_meeting) - n_gram - 1):
        curr_state, next_state = "", ""
        for j in range(n_gram):
            curr_state += cleaned_meeting[i + j] + " "
            next_state += cleaned_meeting[i + j + n_gram] + " "
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


# markov_model = make_markov_model(cleaned_req)
# print("number of states = ", len(markov_model.keys()))

# print("All possible transitions from 'product shall' state: \n")
# print(markov_model['product shall'])

# creates a random sequence from the Markov model which is based on the frequency of words
def generate_service(markov_model, limit=100, start='the'):
    n = 0
    curr_state = start
    next_state = None
    srvs = ""
    srvs += curr_state + " "
    while n < limit:
        next_state = random.choices(list(markov_model[curr_state].keys()),
                                    list(markov_model[curr_state].values()))

        curr_state = next_state[0]
        srvs += curr_state + " "
        n += 1
    return srvs


# for i in range(20):
#   print(str(i)+". ", generate_req(markov_model, start="product shall", limit=12))


meet = "Good Morning News. How are you doing? How are you soon? It's our first from many more meetings are fun and beneficial. Okay. Can I record the meetings? Of course? OK, Google, can you receive describe what you need to do? I want to build a weather station, open up the phone. That's the for the tcsd community. It should be a blog sites where anyone can share their thoughts and problems. They can communicate with others to sounds great. Looks like, when registering a new account the PTSD patients should avoid his username fast with phone number gender, his birthday. The year of his drama and a brief description of his case and whether he is under a doctor's supervision or not, Yes sure. It is an essential Parts. They can also log in as guests to navigate, but not to participate in anything. Yes. He can. He just can't write a comment or enter a room. What do you mean by that? The luggage in users can enter a room based on their gender or age? Is he wants, what does a room the first from a Blog? A room? It's a private face. To people feel more free to share their thoughts. The rooms Edmonds, is the creator of the room. He can invite the admin can make their own private or public. What's the difference between a private room and the public one? A public room will be visible. So that users can request to enter the room while a private one. No one will know our room exists except that users in the room. Can I guess tentaroo know? Okay, how can a user login? Yes, a user can follow. Unfollow, hide orphan users. The application should suggest users with similar cases to login users. In order to connect a user. Can also write whatever he wants in his blog, as long as it means the applications policy. What's the address for the sea? Can we discuss it in the next meeting? I didn't finish. It says you like I can say, we can see the next meeting. Sounds good. When is it going to be? Well, maybe after 2 weeks to schedule. Perfect. Thank you. Anytime. Sorry more functionality before I forget. Yes, of course. What is it? A user can choose whether he wants to be anonymous or not. Okay, that's a pretty good feature to start within the next meeting. Yes. I thought so too. Okay. Thank you. Goodbye. See you soon. "


def gen_seedelements():
    seeds = []
    for actor in actors:
        for verb in verbs:
            seeds.append(actor + ' ' + verb)
    return seeds


def services(meetingscript, actorsstr="", limit=12):
    sysactors = actorsstr.split(",")
    for a in sysactors:
        if a not in actors:
            actors.append(a)
    srvs_arr = []
    cm = clean_txt(meetingscript)
    # cm = clean_txt(read_file(file_path))
    # print('clean text: ', cm)
    mm = make_markov_model(cm)
    # print('model: ', mm)
    seedelements = gen_seedelements()
    for seed in seedelements:
        if seed in mm:
            # print(mm[seed], " ", len(mm[seed]))
            x = len(mm[seed]) * 3
            i = 0
            z = 0
            while i < x:
                z += 1
                # srvs_arr.append(generate_service(mm, start=seed, limit=limit))
                servs = generate_service(mm, start=seed, limit=limit)
                if servs not in srvs_arr:
                    srvs_arr.append(servs)
                    i += 1
                if z > 80:
                    # print("hi ",seed)
                    break
        else:
            continue
    return srvs_arr


#arr = services(meet,"x,y,z")
#for s in arr:
#    print(s)
