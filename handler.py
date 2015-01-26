# -*- coding: utf-8 -*-
"""
Class for handling the data
"""
import urllib
from twitter import *
from tweet import Tweet
from user import User
from corpus import Corpus
import datetime
import xml.etree.ElementTree as ElementTree
import xml.dom.minidom as minidom
import sys


class Handler:

    corpus = Corpus('keys.txt')
    startUser = input('Insert the screen_name of the initial twitter user: ')
    twitter = Twitter(auth=corpus.oAuthDance(corpus.readKeys()))

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
            for hashtag in ttweet['entities']['hashtags']:
                tweet.hashtags.append(hashtag)
            tweet.retweeted = ttweet['retweeted']
            if (not ttweet['in_reply_to_user_id'] is None):
                tweet.isReply = True
                tweet.replyTo = ttweet['in_reply_to_user_id']
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
            user.protected = tUser['protected']
            self.corpus.users.append(user)

    def startHandling(self, name):
        i = 0
        self.addUsers(name)
        for user in self.corpus.users:
            if(not user.protected):
                self.addUserTweets(user)
                print('')
            else:
                continue
        while(True):
            yn = input('Gather new users? [y/n]')
            if (yn is 'y' and not self.corpus.users[i].protected):
                self.startHandling(self.corpus.users[i].screen_name)
                i = i + 1
                break
            elif (yn is 'n'):
                while(True):
                    yn2 = input('Create outputfile? [y/n]')
                    if(yn2 is 'y'):
                        self.createOutputFile()
                        break
                    elif(yn2 is 'n'):
                        break
                    else:
                        print('Please insert y or n')
                break
            else:
                print('Please insert y or n')

    def createOutputFile(self):
        self.createUserEntry()
        string = minidom.parseString(ElementTree.tostring(self.root, encoding='unicode')).toprettyxml()
        output = open('ouput_' + str(datetime.datetime.now()), 'w+')
        output.write(string)
        output.close

    def createUserEntry(self):
        for user in self.corpus.users:
            entry = ElementTree.SubElement(root, 'user')
            ElementTree.SubElement(entry, 'id').text = str(user.uid)
            ElementTree.SubElement(entry, 'name').text = user.name
            ElementTree.SubElement(entry, 'screen name').text = user.screen_name
            ElementTree.SubElement(entry, 'created at').text = user.createdAt
            ElementTree.SubElement(entry, 'description').text = user.description
            ElementTree.SubElement(entry, 'Number of friends').text = str(user.nrFriends)
            ElementTree.SubElement(entry, 'Number of followers').text = str(user.nrFollowers)
            ElementTree.SubElement(entry, 'protected').text = str(user.protected)
            timeline = ElementTree.SubElement(enty, 'timeline')
            tweet = ElementTree.SubElement(timeline, 'tweet')
            for tweetEntry in user.tweets:
                ElementTree.SubElement(tweet, 'id').text = tweetEntry.tid
                ElementTree.SubElement(tweet, 'text').text = tweetEntry.text
                for hashtag in tweetEntry.hashtags:
                    ElementTree.SubElement(tweet, 'hashtag').text = hashtag
                ElementTree.SubElement(tweet, 'created at').text = tweetEntry.createdAt
                ElementTree.SubElement(tweet, 'is retweet').text = str(tweetEntry.retweeted)
                if (tweetEntry.isReply):
                    ElementTree.SubElement(tweet, 'reply to id').text = str(tweetEntry.replyTo)


def main():
    handler = Handler()
    handler.startHandling(handler.startUser)

if __name__ == '__main__':
    main()
