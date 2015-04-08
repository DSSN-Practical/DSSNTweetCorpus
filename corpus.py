# -*- coding: utf-8 -*-

"""
Corpus Module for the DSSNTweetCorpus Project.
It handles the authentification and rate limit handler.
It contains the main array with all users in it as well as the userID array

@author: Robert R.
"""

from twitter import *
import os
import time
import sys


class Corpus:

    FOLLOWER_RATE_LIMIT = 15
    TIMELINE_RATE_LIMIT = 180
    currentTimeline = 0
    currentFollower = 0
    users = []
    ids = []

    def __init__(self, keys):
        """keys.txt is the file that contains the authorization tokens and keys"""
        self.keys = keys

    def readKeys(self):
        """Reads the keys.txt file"""
        k = open(self.keys, 'r', encoding="utf8")
        keys = []
        for line in k:
            if '\n' in line:
                keys.append(line[:-1])
            else:
                keys.append(line)
        return keys

    def oAuthDance(self, keys):
        """OAuth Dance with Twitter"""
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
        """Returns the timeline of a certain user"""
        if self.currentTimeline < self.TIMELINE_RATE_LIMIT:
            timeline = twitter.statuses.user_timeline(screen_name=name, count=3200, since_id=1)
            self.currentTimeline = self.currentTimeline + 1
        else:
            self.halt()
            timeline = self.getUserTimeline(twitter, name)
        return timeline

    def getUserFollowers(self, twitter, name):
        """Returns the Followers of a certain user"""
        if self.currentFollower < self.FOLLOWER_RATE_LIMIT:
            followers = twitter.followers.list(cursor=-1, screen_name=name, count=200, skip_status=True, include_user_entities=True)
            self.currentFollower = self.currentFollower + 1
            print (self.currentFollower)
        else:
            self.halt()
            followers = self.getUserFollowers(twitter, name)
        return followers

    def getIds(self, twitter, ids):
        tweets = twitter.statuses.lookup(id=ids)
        return tweets

    def halt(self):
        """If rate limit is exceeded this method waits 15 minuts"""
        for i in range(900):
            time.sleep(1)
            sys.stdout.write("\rRate limit exceeded, please wait: %d%%" % int(i / 9))
            sys.stdout.flush()
        self.currentTimeline = 0
        self.currentFollower = 0

def main():
    corpus = Corpus('keys.txt')
    twitter = Twitter(auth=corpus.oAuthDance(corpus.readKeys()))
    tweets = corpus.getIds(twitter, input('Insert the tweet IDs: '))
    for tweet in tweets:
        print(tweet['id'] + ':\n')
        print('\t' + tweet['text'])

if __name__ == '__main__':
    main()