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
    visibleFollowers = []
    visibleFriends = []
    nrFriends = 0
    nrFollowers = 0
    tweets = []
    #only used for GET timeline
    protected = False