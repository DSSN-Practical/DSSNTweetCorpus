# -*- coding: utf-8 -*-
"""
Friender class creating randomly friendrequests for users to create more meta-data
"""
import random


class Friender:

    def __init__(self, corpus):
        """Corpus must be not empty"""
        self.corpus = corpus

    def setUserFriends(self, user):
        """Set a random sample of users as friends of a certain user"""
        if len(user.tweets) <= len(self.corpus.ids):
            user.friends = random.sample(self.corpus.ids, random.randint(1, len(user.tweets)))
        else:
            user.friends = random.sample(self.corpus.ids, random.randint(1, len(self.corpus.ids)))

    def setUserFriendrequests(self, user):
        """For each friend assign one Tweet as a friendrequest"""
        requests = random.sample(user.tweets, len(user.friends))
        for i, request in enumerate(requests):
            request.isFriendRequest = True
            request.friendRequestToId = user.friends[i]

    def friendHandler(self):
        """General method that handles the friends"""
        for user in self.corpus.users:
            if len(user.tweets) > 1:
                self.setUserFriends(user)
                self.setUserFriendrequests(user)
            else:
                user.friends = []