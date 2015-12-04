# -*- coding: utf-8 -*-
"""
Agent class accessing the XODX APO
"""
from collections import namedtuple
import time

class Agent():

    def __init__(self, text):
        self.text = text

    def handle(self):
        start = False
        tStart = 0
        tEnd = 0
        timeline = []
        for i, line in enumerate(self.text):
            if '<timeline>' in line:
                start = True
            if '<tweet>' in line:
                tStart = i + 1
            if '</tweet>' in line:
                tEnd = i - 1
            if start and tEnd != 0:
                timeline.append(self.analyzeTweet(self.text[tStart:tEnd]))
                tStart = 0
                tEnd = 0
        return timeline

    def simulateAgent(self, timeline):
        time.sleep(int(timeline[0].deltaTime))
        self.createPost(timeline[0].text)
        if timeline[0].followRequestToId != None:
            self.follow(timeline[0].followRequestToId)
        for i, tweet in enumerate(timeline[1:]):
            print(tweet.deltaTime + '   ' + timeline[i].deltaTime)
            time.sleep(int(tweet.deltaTime) - int(timeline[i].deltaTime))
            self.createPost(tweet.text)
            if tweet.followRequestToId != None:
                self.follow(tweet.followRequestToId)

    def createPost(self, text):
        """
        Placeholder
        :param text:
        :return:
        """
        print('Post: ' + text)

    def follow(self, userID):
        """
        Placeholder
        :param userID:
        :return:
        """
        print('Follow: ' + userID)

    def unfollow(self, userID):
        """
        Placeholder
        :param userID:
        :return:
        """
        print('Unfollow: ' + userID)

    def deletePost(self, postID):
        """
        Placeholder
        :param postID:
        :return:
        """
        print(postID + ' was deleted.')

    def analyzeTweet(self, tweet):
        """
        Analyzes the tweet part of the timeline
        :param tweet:
        :return Tweet:
        """
        Tweet = namedtuple('Tweet', 'tid, text, replyToID, followRequestToId, deltaTime')
        Tweet.text = ''
        for i, line in enumerate(tweet):
            if '<id>' in line:
                Tweet.tid = tweet[i+1]
            if '<text>' in line:
                for subLine in tweet[i+1:]:
                    if  not '</text>' in subLine:
                        Tweet.text = Tweet.text + subLine
                    else:
                        break
            if '<reply_to_id>' in line:
                Tweet.replyToID = tweet[i+1]
            if '<followrequest_to_id>' in line:
                Tweet.followRequestToId = tweet[i+1]
            if '<delta>' in line:
                Tweet.deltaTime = tweet[i+1]
        return Tweet