# -*- coding: utf-8 -*-
"""
Object class for tweets
"""

class Tweet(object):

    id = 0
    text = ''
    screen_name = ''
    hashtags = []
    isRT = False
    isFriendRequest = False

    def __init__(self, id):
        self.id = id