# -*- coding: utf-8 -*-
"""
Object class for tweets
"""


class Tweet(object):

    tid = 0
    text = ''
    createdAt = ''
    isReply = False
    replyTo = None
    retweeted = False
    #nto for now causes errors
    hashtags = []