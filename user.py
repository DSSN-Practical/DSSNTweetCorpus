# -*- coding: utf-8 -*-
"""
Object class User contains all relevant meta-data of a single user

@author: Robert R.
"""


class User(object):

    uid = 0
    screen_name = ''
    name = ''
    createdAt = ''
    description = ''
    nrFriends = 0
    #currently not used
    nrFollowers = 0
    tweets = []
    followers = []
    deltaTime = 0
    #only used for GET timeline
    protected = False