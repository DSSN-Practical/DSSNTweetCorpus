# -*- coding: utf-8 -*-
"""
Object class User
"""


class User(object):

    uid = 0
    screen_name = ''
    name = ''
    createdAt = ''
    description = ''
    nrFriends = 0
    nrFollowers = 0
    tweets = []
    friends = []
    #only used for GET timeline
    protected = False