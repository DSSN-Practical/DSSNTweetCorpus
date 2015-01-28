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
import time
import sys
#from tweet import Tweet
#from user import User
#import urllib
#import shutil


class Corpus:

    FOLLOWER_RATE_LIMIT = 180
    TIMELINE_RATE_LIMIT = 15
    currentTimeline = 0
    currentFollower = 0
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
        if self.currentTimeline < self.TIMELINE_RATE_LIMIT:
            timeline = twitter.statuses.user_timeline(screen_name=name)
            self.currentTimeline = self.currentTimeline + 1
        else:
            self.halt()
            self.getUserTimeline(twitter, name)
        return timeline

    def getUserFollowers(self, twitter, name):
        if self.currentFollower < self.FOLLOWER_RATE_LIMIT:
            followers = twitter.followers.list(cursor=-1, screen_name=name, count=200, skip_status=True, include_user_entities=True)
            self.currentFollower = self.currentFollower + 1
        else:
            self.halt()
            self.getUserFollowers(twitter, name)
        return followers

    def halt(self):
        print('Rate limit exceeded, please wait:\n')
        for i in range(900):
            time.sleep(1)
            sys.stdout.write("\r%d%%" % int(i / 9))
            sys.stdout.flush()
        self.currentTimeline = 0
        self.currentFollower = 0