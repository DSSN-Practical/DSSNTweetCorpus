# -*- coding: utf-8 -*-
"""
Object class for tweets which contains data of a single tweet.

@author: Robert R.
"""


class Tweet(object):

    tid = 0
    text = ''
    createdAt = ''
    isReply = False
    replyTo = None
    retweeted = False
    isFriendRequest = False
    friendRequestToId = 0
    #nto for now causes errors
    hashtags = []