# -*- coding: utf-8 -*-
"""
Object class User
"""

class User(object):

    id = 0
    screen_name = ''
    followers = ''
    createdAt = ''
    followers = []
    friends = []
    nrFriends = len(friends)
    nrFollowers = len(followers)

    def __init__(self):
        self.id = id