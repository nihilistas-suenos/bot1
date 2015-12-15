"""
twitterbot version 1.0
"""
from logic import *
from twython import Twython, TwythonError
from sys import argv

"""	
Get info:

> import twython
> from twython import Twython as T
> help(twython.api)
> help(T.get_favourites) # example

"""

#################
# MAIN FUNCTION #
#################


def main():
        
        try:		
        		index = ""
        		
    			while 1:
                        	username = ""
                        	if index == "":
                        		t,username = set_params()
                        	opcion = options()
                        	if opcion == "1":
                                	wrap_favs(user_db,username,t)
                        	elif opcion == "2":
                                	mssg = 0
                                	while mssg == 0:
                                		mssg = send_tweet(t)
                        	elif opcion == "0": exit(0)
                        	elif opcion == "-1": index = ""
                                
        except TwythonError as e: print (e)



if __name__ == "__main__":
        main()

  
