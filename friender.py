# -*- coding: utf-8 -*-
"""
Friender class creating randomly friendrequests for users to create more meta-data
"""
import random


class Friender:

    def __init__(self, corpus):
        """Corpus must be not empty"""
        self.corpus = corpus

    def setUserFollowers(self, user):
        """Set a random sample of users as friends of a certain user"""
        if len(user.tweets) <= len(self.corpus.ids):
            user.followers = random.sample(self.corpus.ids, random.randint(1, len(user.tweets)))
        else:
            user.followers = random.sample(self.corpus.ids, random.randint(1, len(self.corpus.ids)))

    def setUserFollowerrequests(self, user):
        """For each friend assign one Tweet as a friendrequest"""
        requests = random.sample(user.tweets, len(user.followers))
        for i, request in enumerate(requests):
            request.isFollowRequest = True
            request.followRequestToId = user.followers[i]

    def followHandler(self):
        """General method that handles the friends"""
        for user in self.corpus.users:
            if len(user.tweets) > 1:
                self.setUserFollowers(user)
                self.setUserFollowerrequests(user)
            else:
                user.followers = []