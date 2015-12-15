#!/usr/bin/python

import pickle

basic = ["#hashtag1","#hashtag2","#hashtag3"]
count1 = ["#hashtag4"]
count2 = ["hashtag5"]
hashtags = {"count1": basic + count1,"count2": basic + count2}


with open("hashtags.pickle","wb") as handle:
	pickle.dump(hashtags,handle)
