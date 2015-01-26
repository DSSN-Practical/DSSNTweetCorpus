# -*- coding: utf-8 -*-
"""
Object class for tweets
"""


class Tweet(object):

    tid = 0
    text = ''
    hashtags = []
    createdAt = ''
    isReply = False
    replyTo = None
    retweeted = False