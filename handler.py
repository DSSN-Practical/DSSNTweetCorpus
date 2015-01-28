# -*- coding: utf-8 -*-
"""
Class for handling the data
"""
from user import User
from tweet import Tweet
from corpus import Corpus
from friender import Friender
from twitter import *
from bs4 import BeautifulSoup
#See http://www.crummy.com/software/BeautifulSoup/

import urllib
import datetime
import xml.etree.ElementTree as ElementTree
import sys


class Handler:

    corpus = Corpus('keys.txt')
    startUser = input('Insert the screen_name of the initial twitter user: ')
    twitter = Twitter(auth=corpus.oAuthDance(corpus.readKeys()))
    steps = int(input('Insert the amount of recursions: '))

    def __init__(self):
        self.root = ElementTree.Element('file')

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

            #doesn't work for now'
            #for hashtag in ttweet['entities']['hashtags']:
            #    tweet.hashtags.append(hashtag)
            tweet.retweeted = ttweet['retweeted']
            if (not ttweet['in_reply_to_user_id'] is None):
                tweet.isReply = True
                tweet.replyTo = ttweet['in_reply_to_user_id']
            user.tweets.append(tweet)

    def addUsers(self, name):
        try:
            followers = self.corpus.getUserFollowers(self.twitter, name)
        except urllib.request.HTTPError:
            print('An Error Occured, please restart the application.')
        for tUser in followers['users']:
            user = User()
            iid = tUser['id']
            if (iid in self.corpus.ids):
                print('ding')
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
                user.protected = tUser['protected']
                self.corpus.users.append(user)

    def startHandling(self, name):
        self.addUsers(name)
        for i in range(self.steps):
            if (self.corpus.users[i].protected):
                continue
            else:
                self.addUsers(self.corpus.users[i].screen_name)
            #yn = input('\nGather new users? [y/n]:\t')
            #if (not self.corpus.users[i].protected):
                #i = i + 1
                #self.startHandling(self.corpus.users[i].screen_name)
                #break
        print('Reading tweets from all users, please wait:\n')
        for k, user in enumerate(self.corpus.users):
            if(not user.protected):
                self.addUserTweets(user)
            sys.stdout.write("\r%d%%" % int((k * 100) / len(self.corpus.users)))
            sys.stdout.flush()
        friender = Friender(self.corpus)
        friender.friendHandler()
        for user in self.corpus.users:
            self.createUserEntry(user)
        while(True):
            yn = input('\nCreate outputfile? [y/n]:\t')
            if(yn is 'y'):
                self.createOutputFile()
                break
            elif(yn is 'n'):
                break
            else:
                print('Please insert y or n')

    def createOutputFile(self):
        xmlString = ElementTree.tostring(self.root, encoding="UTF-8")
        string = BeautifulSoup(xmlString).prettify()
        output = open('output_' + str(datetime.datetime.now()) + '.xml', 'w+')
        output.write(string)
        output.close

    def createUserEntry(self, user):
        entry = ElementTree.SubElement(self.root, 'user')
        ElementTree.SubElement(entry, 'id').text = str(user.uid)
        ElementTree.SubElement(entry, 'name').text = str(user.name)
        ElementTree.SubElement(entry, 'screen_name').text = str(user.screen_name)
        ElementTree.SubElement(entry, 'created_at').text = str(user.createdAt)
        ElementTree.SubElement(entry, 'description').text = str(user.description)
        ElementTree.SubElement(entry, 'Number_of_friends').text = str(user.nrFriends)
        ElementTree.SubElement(entry, 'Number_of_followers').text = str(user.nrFollowers)
        ElementTree.SubElement(entry, 'protected').text = str(user.protected)
        if (len(user.friends) > 0):
            friends = ElementTree.SubElement(entry, 'friends')
            for friend in user.friends:
                ElementTree.SubElement(friends, 'id').text = str(friend)
        if (len(user.tweets) > 0):
            timeline = ElementTree.SubElement(entry, 'timeline')
            for tweetEntry in user.tweets:
                tweet = ElementTree.SubElement(timeline, 'tweet')
                ElementTree.SubElement(tweet, 'id').text = str(tweetEntry.tid)
                ElementTree.SubElement(tweet, 'text').text = tweetEntry.text
                ElementTree.SubElement(tweet, 'created_at').text = str(tweetEntry.createdAt)
                ElementTree.SubElement(tweet, 'is_retweet').text = str(tweetEntry.retweeted)
                if (tweetEntry.isFriendRequest):
                        ElementTree.SubElement(tweet, 'friendrequest_to_id').text = str(tweetEntry.FriendRequestToId)
                if (tweetEntry.isReply):
                    ElementTree.SubElement(tweet, 'reply_to_id').text = str(tweetEntry.replyTo)
                #for hashtag in tweetEntry.hashtags:
                #    ElementTree.SubElement(tweet, 'hashtag').text = str(hashtag)


def main():
    handler = Handler()
    handler.startHandling(handler.startUser)

if __name__ == '__main__':
    main()
