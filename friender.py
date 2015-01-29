# -*- coding: utf-8 -*-

#from tweet import Tweet
#from user import User
#from corpus import Corpus
import random


class Friender:

    def __init__(self, corpus):
        self.corpus = corpus

    def setUserFriends(self, user):
        if len(user.tweets) <= len(self.corpus.ids):
            user.friends = random.sample(self.corpus.ids, random.randint(1, len(user.tweets)))
        else:
            user.friends = random.sample(self.corpus.ids, random.randint(1, len(self.corpus.ids)))

    def setUserFriendrequests(self, user):
        requests = random.sample(user.tweets, len(user.friends))
        for i, request in enumerate(requests):
            request.isFriendRequest = True
            request.FriendRequestToId = user.friends[i]

    def friendHandler(self):
        for user in self.corpus.users:
            if len(user.tweets) > 1:
                self.setUserFriends(user)
                self.setUserFriendrequests(user)
            else:
                user.friends = []