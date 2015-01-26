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

    def addUserTweets(self, user):
        try:
            timeline = self.corpus.getUserTimeline(self.twitter, user.screen_name)
        except urllib.request.HTTPError:
            print('An Error Occured, please restart the application.')
        for ttweet in timeline:
            tweet = Tweet()
            tweet.tid = ttweet['id']
            tweet.text = ttweet['text']
            tweet.createdAt = ttweet['created_at']
            for hashtag in ttweet['hashtags']:
                tweet.hashtags.append(hashtag)
            tweet.retweeted = ttweet['retweeted']
            if (not ttweet['in_reply_to_user_id_str'] is None):
                tweet.isReply = True
                tweet.replyTo = ttweet['in_reply_to_user_id_str']
            user.tweets.append(tweet)

    def addUsers(self, name):
        try:
            followers = self.twitter.followers.list(cursor=-1, screen_name=name, count=200, skip_status=True, include_user_entities=True)
        except urllib.request.HTTPError:
            print('An Error Occured, please restart the application.')
        for tUser in followers['users']:
            user = User()
            iid = tUser['id']
            if (iid in self.corpus.ids):
                continue
            else:
                user.uid = iid
                self.corpus.ids.append(iid)
            user.screen_name = tUser['screen_name']
            user.name = tUser['name']
            user.description = tUser['description']
            user.createdAt = tUser['created_at']
            user.nrFriends = tUser['friends_count']
            user.nrFollowers = tUser['followers_count']
            self.corpus.users.append(user)

    def startHandling(self, name):
        self.addUsers(name)
        i = 0
        for user in self.corpus.users:
            self.addUserTweets(user.screen_name)
        if (input('Gather new users? [y/n]') is 'y'):
            self.startHandling(self.corpus.users[i].screen_name)


def main():
    handler = Handler()
    handler.addUsers(handler.startUser)
    for user in handler.corpus.users:
        print (user.name + ': ' + user.description)

if __name__ == '__main__':
    main()
