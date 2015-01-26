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
        try:
            followers = self.twitter.followers.list(cursor=-1, screen_name=name,count = 200, skip_status=True, include_user_entities=True)
        except urllib.request.HTTPError:
            print('An Error Occured, please restart the application.')
        for tUser in followers['users']:
            user = User()
            user.tid = tUser['id']
            user.screen_name = tUser['screen_name']
            user.name = tUser['name']
            user.description = tUser['description']
            user.createdAt = tUser['created_at']
            user.nrFriends = tUser['friends_count']
            user.nrFollowers = tUser['followers_count']
            self.corpus.users.append(user)


def main():
    handler = Handler()
    handler.addUsers(handler.startUser)
    for user in handler.corpus.users:
        print (user.name + ': ' + user.description)

if __name__ == '__main__':
    main()
