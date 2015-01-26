# -*- coding: utf-8 -*-

"""
Corpus Module for the DSSNTweetCorpus Project
This Module contains the main function and should be called as the main class for this project.

Currently it just gives an outputstream of all current public tweets with '#vote5sos' in it,
since it is the most popular hashtag for now. This project is not done and will need a proper
object to handle the tweets with their usernames, id's etc.

Need to figure out how the Bot is handling the text and how the text should be formatted.

Dependencies:     python twitter API-tools from: http://mike.verdone.ca/twitter/
                  consumer keys and tokens for the APP in order to use twitters API

Problems:  Rate limit. Rate limit is set for a 15 minute window. statuses calls are limited to
           180 calls, friends / followers calls to 30.

@author: Robert R.
"""

from twitter import *
import os
from tweet import Tweet
from user import User
#import urllib
#import shutil


class Corpus:

    users = []
    ids = []

    def __init__(self, keys):
        self.keys = keys

    def readKeys(self):
        k = open(self.keys, 'r', encoding="utf8")
        keys = []
        for line in k:
            if '\n' in line:
                keys.append(line[:-1])
            else:
                keys.append(line)
        return keys

    def oAuthDance(self, keys):
        MY_TWITTER_CREDS = os.path.expanduser('~/.my_app_credentials')
        CONSUMER_KEY = keys[0]
        CONSUMER_SECRET = keys[1]
        oauth_token = keys[2]
        oauth_token_secret = keys[3]
        if not os.path.exists(MY_TWITTER_CREDS):
            oauth_dance("DSSNTweetCorpus", CONSUMER_KEY, CONSUMER_SECRET, MY_TWITTER_CREDS)
        auth = OAuth(oauth_token, oauth_token_secret, CONSUMER_KEY, CONSUMER_SECRET)
        return auth

    def getUserTimeline(self, twitter, name):
        timeline = twitter.statuses.user_timeline(screen_name=name)
        return timeline

    def getUserFollowers(self, twitter, name):
        followers = twitter.followers.list(cursor=-1, screen_name=name, skip_status=True, include_user_entities=False)
        return followers


"""
------------------------------------
----------- Old & Unused -----------
------------------------------------

    def outputUserTimeline(self, twitter, name):
        tweets = t.statuses.user_timeline(screen_name=name)
        for tweet in tweets:
            print(str(tweet['user']['screen_name']) + '\t' + str(tweet['created_at']) + '\t' + str(tweet['user']['time_zone']) + ':\n' + str(tweet['text']))

    #creating a raw output of tweets
    def outputStream(self, auth):
        twitter_stream = TwitterStream(auth=auth, domain='stream.twitter.com')
        stream = twitter_stream.statuses.sample()
        for tweet in stream:
            if 'text' in tweet:
                #just to filter some tweets
                if 'gameinsight' in tweet['text']:
                    print(tweet['user']['screen_name'] + ':\n' + tweet['text'] + '\n\n')
"""

def main():
    corpus = Corpus('keys.txt')
    name = 'white_gecko'
    twitter = Twitter(auth=auth)
    corpus.outputUserTimeline(corpus.oAuthDance(corpus.readKeys()), name)
    for user in corpus.returnUserFollowers(corpus.oAuthDance(corpus.readKeys()), name):
        if (not user['protected']):
            corpus.outputUserTimeline(corpus.oAuthDance(corpus.readKeys()), user['screen_name'])

#call if module is called as main
if __name__ == '__main__':
    main()
