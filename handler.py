# -*- coding: utf-8 -*-
"""
Class for handling the data. It contains the __main__ method.
This class is used for getting meta-data from Twitter and create respectively
user and tweet objects.

Dependencies:     python twitter API-tools from: http://mike.verdone.ca/twitter/
                  Beautifulsauce for XML parsing from: http://www.crummy.com/software/BeautifulSoup/
                  consumer keys and tokens for the APP in order to use twitters API

@author: Robert R.
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
from dateutil.parser import parse
import xml.etree.ElementTree as ElementTree
import sys
import os


class Handler:
    """Authentification, prompt for initial user and prompt for iterations on creating the object"""

    corpus = Corpus('keys.txt')
    startUser = input('Insert the screen_name of the initial twitter user: ')
    twitter = Twitter(auth=corpus.oAuthDance(corpus.readKeys()))
    steps = int(input('Insert the amount of iterations: '))
    maxtime = int(input('Insert the respective time (in days)')) * 86400

    def __init__(self):
        self.root = ElementTree.Element('file')

    def addUserTweets(self, user):
        """Gets the tweets from a user via its timeline and creates a Tweet object each time"""
        try:
            timeline = self.corpus.getUserTimeline(self.twitter, user.screen_name)
        except urllib.request.HTTPError:
            print('An Error Occured, please restart the application.')
        tweets = []
        for ttweet in timeline:
            tweet = Tweet()
            tweet.tid = ttweet['id']
            tweet.text = ttweet['text']
            tweet.createdAt = ttweet['created_at']
            tweet.retweeted = ttweet['retweeted']
            if (not ttweet['in_reply_to_user_id'] is None):
                tweet.isReply = True
                tweet.replyTo = ttweet['in_reply_to_user_id']
            tweets.append(tweet)
        user.tweets = self.createDeltaTimes(tweets)

    def createDeltaTimes(self, tweets):
        if(len(tweets) > 0):
            delta = parse(tweets[0].createdAt) - parse(tweets[-1].createdAt)
            for i, tweet in enumerate(tweets):
                if i == 0:
                    tweet.deltaTime = 0
                else:
                    subdelta = parse(tweet.createdAt) - parse(tweets[0].createdAt)
                    percentage = subdelta.total_seconds() / delta.total_seconds()
                    tweet.deltaTime = int(self.maxtime * abs(percentage))
        return tweets

    def addUsers(self, name):
        """Get followers of a certain user and add it to the corpus.users array"""
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

    def createDir(self):
        outDir = 'output' + str(datetime.datetime.now())
        if not os.path.exists(outDir):
            os.makedirs(outDir)
        return outDir

    def startHandling(self, name):
        """General method to handle all data"""
        self.addUsers(name)
        for i in range(self.steps):
            if (self.corpus.users[i].protected):
                continue
            else:
                self.addUsers(self.corpus.users[i].screen_name)
        for k, user in enumerate(self.corpus.users):
            if(not user.protected):
                self.addUserTweets(user)
            sys.stdout.write("\rReading tweets from all users, please wait: %d%%" % int((k * 100) / len(self.corpus.users)))
            sys.stdout.flush()
        friender = Friender(self.corpus)
        friender.followHandler()
        while(True):
            mode = input('\nSelect mode:\n\n[p] Print all data in the console\n[o] Create an outputfile\n[q] Quit')
            if mode == 'p':
                self.printData()
                break
            elif mode == 'o':
                outDir = self.createDir()
                for j, user in enumerate(self.corpus.users):
                    self.createOutputFile(user, self.createUserEntry(user), outDir)
                    print ('Created user Entry for: ' + str(j))
                #self.createOutputFile()
                break
            elif mode == 'q':
                break

    def createOutputFile(self, user, soup, outDir):
        """Creates the outputfile"""
        #xmlString = ElementTree.tostring(self.root, encoding="UTF-8")
        #string = BeautifulSoup(xmlString).prettify()
        output = open(outDir + '/' + user.screen_name + '.xml', 'w+')
        output.write(soup.prettify())
        output.close

    def createUserEntry(self, user):
        """Creates an entry for a user"""
        """
        soup = BeautifulSoup(features='xml')
        soup.append(soup.new_tag('id'))
        soup.id.append(str(user.uid))
        soup.append(soup.new_tag('user_name'))
        soup.user_name.append(str(user.name))
        soup.append(soup.new_tag('screen_name'))
        soup.screen_name.append(str(user.screen_name))
        soup.append(soup.new_tag('created_at'))
        soup.created_at.append(str(user.createdAt))
        soup.append(soup.new_tag('description', str(user.description)))
        soup.description.append(str(user.description))
        if (len(user.followers) > 0):
            soup.append(soup.new_tag('followers'))
            for i, follower in enumerate(user.followers):
                soup.followers.append(soup.new_tag('follower_id'))
                soup.follower_id.insert(i + 1, str(follower))
        if (len(user.tweets) > 0):
            soup.append(soup.new_tag('timeline'))
            for tweetEntry in user.tweets:
                soup.timeline.append(soup.new_tag('tweet'))
                soup.tweet.append(soup.new_tag('tweet_id'))
                soup.tweet_id.append(str(tweetEntry.tid))
                soup.tweet.append(soup.new_tag('tweet_text'))
                soup.tweet_text.append(str(tweetEntry.text))
                soup.tweet.append(soup.new_tag('tweet_time'))
                soup.tweet_time.append(str(tweetEntry.createdAt))
                if (tweetEntry.isFollowRequest):
                    soup.tweet.append(soup.new_tag('is_followrequest'))
                    soup.is_followrequest.append(str(tweetEntry.isFollowRequest))
                    soup.tweet.append(soup.new_tag('follow_request_id'))
                    soup.follow_request_id.append(str(tweetEntry.followRequestToId))
        """
        entry = ElementTree.SubElement(self.root, 'user')
        ElementTree.SubElement(entry, 'id').text = str(user.uid)
        ElementTree.SubElement(entry, 'name').text = str(user.name)
        ElementTree.SubElement(entry, 'screen_name').text = str(user.screen_name)
        ElementTree.SubElement(entry, 'created_at').text = str(user.createdAt)
        ElementTree.SubElement(entry, 'description').text = str(user.description)
        #ElementTree.SubElement(entry, 'Number_of_friends').text = str(user.nrFriends)
        #ElementTree.SubElement(entry, 'Number_of_followers').text = str(user.nrFollowers)
        ElementTree.SubElement(entry, 'protected').text = str(user.protected)
        if (len(user.followers) > 0):
            followers = ElementTree.SubElement(entry, 'followers')
            for follower in user.followers:
                ElementTree.SubElement(followers, 'id').text = str(follower)
        if (len(user.tweets) > 0):
            timeline = ElementTree.SubElement(entry, 'timeline')
            for tweetEntry in user.tweets:
                tweet = ElementTree.SubElement(timeline, 'tweet')
                ElementTree.SubElement(tweet, 'id').text = str(tweetEntry.tid)
                ElementTree.SubElement(tweet, 'text').text = tweetEntry.text
                ElementTree.SubElement(tweet, 'created_at').text = str(tweetEntry.createdAt)
                ElementTree.SubElement(tweet, 'delta').text = str(tweetEntry.deltaTime)
                ElementTree.SubElement(tweet, 'is_retweet').text = str(tweetEntry.retweeted)
                if (tweetEntry.isFollowRequest):
                        ElementTree.SubElement(tweet, 'followrequest_to_id').text = str(tweetEntry.followRequestToId)
                if (tweetEntry.isReply):
                    ElementTree.SubElement(tweet, 'reply_to_id').text = str(tweetEntry.replyTo)
                #for hashtag in tweetEntry.hashtags:
                #    ElementTree.SubElement(tweet, 'hashtag').text = str(hashtag)
        soup = BeautifulSoup(ElementTree.tostring(self.root, encoding="UTF-8"), features='xml')
        self.root.clear()
        return soup

    def printData(self):
        """Prints the raw data in the terminal"""
        for i, user in enumerate(self.corpus.users):
            print('User #' + str(i + 1) + ':')
            print('\tID:\t\t' + str(user.uid))
            print('\tScreen Name:\t' + str(user.screen_name))
            print('\tName:\t' + str(user.name))
            print('\tCreated at:\t' + str(user.createdAt))
            print('\tDescription:\t' + str(user.description))
            print('\tProtected:\t' + str(user.protected))
            print('\tFriends:\t')
            for k, friend in enumerate(user.friends):
                print('\t\tFriend #' + str(k + 1) + ':\t' + str(friend))
            print('\tTimeline:')
            for j, tweet in enumerate(user.tweets):
                print('\t\tTweet #' + str(j + 1) + ':')
                print('\t\tID:\t\t' + str(tweet.tid))
                print('\t\tCreated at:\t' + str(tweet.createdAt))
                if(tweet.isReply):
                    print('\t\tReply to ID:\t' + str(tweet.replyTo))
                if(tweet.isFriendRequest):
                    print('\t\tFriendrequest to ID:\t' + str(tweet.friendRequestToId))
            print('==============================================')


def main():
    handler = Handler()
    handler.startHandling(handler.startUser)

if __name__ == '__main__':
    main()
