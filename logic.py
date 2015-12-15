#!/usr/bin/python

from logic import *
import datetime
import twython
from twython import Twython, TwythonError
import time
import random
from random import randrange
import subprocess as sub
import sys
import pickle

global t

###########################################
# GET HELP ABOUT DEFAULT METHODS: help(t) #
###########################################



def options():
	print "\nOPTIONS:"
  	print "  1) Generate favs from hashtag"
   	print "  2) Publish new tweet"
  	print "  3) Get friends"
   	print "  0) Exit"
   	print " -1) Change profile"
	opcion = raw_input("\nSelect an option: ")
	return opcion
	
def send_tweet(t):
	mssg = raw_input("Introduce the message:\n")
	if len(mssg) < 150:
		t.update_status(status=mssg)
		return 1
	else:
		print "Must be shorter than 160 chars."
		return 0

with open("hashtags.pickle","rb") as handle:
	hashtags = pickle.load(handle)


# FUNCTIONS

def get_usrIDs():

	CONFIG_PARAMS = {}
	with open("twitter_counts.txt") as counts:
        	for i in counts:
        	        l = i.split(" ")
                	l[-1] = l[-1].rstrip('\n')
                	CONFIG_PARAMS[l[1]] = l[2:]
	return CONFIG_PARAMS.keys()




def read_db(db_file):
        user_db = []
        with open(db_file) as db:
                for i in db:
                        user_db.append(int(i[:-1]))
        return user_db

user_db = read_db("users_db.txt")


def set_parameters(user,filename = "twitter_counts.txt"):
        CONFIG_PARAMS = {}
        with open(filename) as counts:
                for i in counts:
                        l = i.split(" ")
                        if len(l) == 6:
                                l[-1] = l[-1].rstrip('\n')
                                CONFIG_PARAMS[l[1]] = l[2:]
        

        APP_KEY = CONFIG_PARAMS[user][0]
        APP_SECRET = CONFIG_PARAMS[user][1]
        OAUTH_TOKEN = CONFIG_PARAMS[user][2]
        OAUTH_TOKEN_SECRET = CONFIG_PARAMS[user][3]

        t = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

        return t

def set_params():
	users = get_usrIDs()
	print("\n    AVAILIBLE PROFILES:")
	for i in range(len(users)):
		print "[" + str(i) + "]", users[i]
	index = int(raw_input("\nPlease select one user (number): "))
	username = users[index]
	t = set_parameters(users[index])
	return t


def shuffle(items):  # mutates input list
        i = len(items)
        while i > 1:
                j = randrange(i)  # 0 <= j <= i
                items[j], items[i] = items[i], items[j]
                i = i - 1
                return

def show_keys(diccionario):
        print "\n    OPTION KEYS\n"
        for k in diccionario.keys():
                print "[X]", k
        print "\n"

def show_list(list_name):
        print "\n   LIST ELEMENTS"
        n = len(list_name)
        for i in range(n):
                print "[X]", list_name[i]
        print ""
        
def add_friend(t,usr_ID):
        if  usr_ID not in user_db:
                new_friend = t.create_friendship(user_id = int(usr_ID))
                if new_friend["following"] == "true":
                        print "\tNew friend: ",usr_ID
        
def user_quality_tweet(tweet):
        """
        This function allows to check if a user tend to follow.
        """
        owner = tweet["user"]
        followers = owner["followers_count"]
        friends = owner["friends_count"]
        if int(followers) > 0:
                rr_val = float(friends)/int(followers)
                return rr_val                                        


def user_quality_id(usr_id):
        """
        This function allows to check if a user tend to follow.
        """
        usr = t.show_user(user_id = usr_id)
        followers = usr["followers_count"]
        friends = usr["friends_count"]
        if int(friends) > 0:
                rr_val = float(followers)/int(friends)
                return rr_val 


def get_timeline(t,usr_id, n = 20):
        tl = t.get_user_timeline(user_id = usr_id,count = n)
        return tl


def favorite_tweet(t,tweet):
        if tweet["favorited"] == False:
                fav = t.create_favorite(id = int(tweet["id"]))
                if tweet["retweet_count"] >= 1000:
                        t.retweet(id = int(tweet["id"]))
        # else: print "Previously marked as favourite."


def favorite_tl(t,usr_id, n=3):
        tl = get_timeline(t,usr_id)
        number_tweets = len(tl)
        vals = []
        for i in range(n):
                randomval = int((random.random() * number_tweets) % number_tweets)
                if randomval not in vals:
                        vals.append(randomval)
                        favorite_tweet(t,tl[randomval])
        
def search_term(t, term, n = 300):
        search = t.search(q = term, result_type="recent",count = n)
        return search[search.keys()[1]]



def mark_favorites(t,id_list, usr_db):
        print "\n    USERS FAV ADDED"
        index = random.shuffle([x for x in range(len(id_list))])
        for i in id_list:
                if i not in usr_db:
                        favorite_tl(t,usr_id = i)
                        with open("users_db.txt","a") as db:
                                db.write(str(i) + "\n")
                        print "[X]",i
                        st = int(random.random() * 10) % 3
                        time.sleep(st + 5)
                else:
                        print "[X]",i,"*"
        print "\n" 


def ids_from_search(t,tweets):
        user_ids = []
        for i in range(len(tweets)):
                qual = user_quality_tweet(tweets[i])
                if qual >= 2:
                        user_ids.append(tweets[i]["user"]["id"])
                if qual <= 0.2:
                        add_friend(t,tweets[i]["user"]["id"])
        return set(user_ids)


def wrap_favs(user_db,user,t):
        #global termino
        #if termino == "":
        terms = hashtags[user]
        terms = random.sample(terms,3)
        #termino = raw_input("\nKeyword for searching? ")
                        
        # perform a search and get user ids:
        for termino in terms:
                print "Running:",termino
                tweets = search_term(t,term = termino, n = 600)
                ids = list(ids_from_search(t,tweets))

        
                # resort ids:
                ids = set(list(random.sample(ids,len(ids))))
                print "Recopiled profiles: ", len(ids)

        
                # mark favorites:
                mark_favorites(t,ids ,user_db)
