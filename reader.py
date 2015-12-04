# -*- coding: utf-8 -*-
"""
Reader class reading out the XML-files
"""
import os
from agent import Agent

class Reader:

    def __init__(self, folder):
        self.folder = folder

    def readFile(self, file):
        f = open(file, 'r', encoding="utf8")
        text = []
        for line in f:
            text.append(line)
        f.close()
        return text

    def readInputFiles(self):
        files = os.listdir(self.folder)
        users = []
        for entry in files:
            users.append(self.readFile(self.folder + '/' + entry))
        return users

def main():
    reader = Reader(input('Foldername: '))
    users = reader.readInputFiles()
    for user in users:
        agent = Agent(user)
        agent.simulateAgent(agent.handle())

if __name__ == '__main__':
    main()