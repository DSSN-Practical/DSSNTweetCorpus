# -*- coding: utf-8 -*-
"""
Class for handling the data
"""
import urllib
from twitter import *
from tweet import Tweet
from user import User
from corpus import Corpus


class Handler:

    corpus = Corpus('keys.txt')
    startUser = input('Insert the screen_name of the initial twitter user: ')
    twitter = Twitter(auth=corpus.oAuthDance(corpus.readKeys()))

    def addUserTweets(self, name):
        try:
            timeline = self.corpus.getUserTimeline(self.twitter, name)
        except urllib.request.HTTPError:
            print('An Error Occured, please restart the application.')

    def addUsers(self, name):
        followers = self.twitter.followers.list(cursor=-1, screen_name=name, skip_status=True, include_user_entities=True)
        print (followers)


def main():
    handler = Handler()
    handler.addUsers(handler.startUser)

if __name__ == '__main__':
    main()
