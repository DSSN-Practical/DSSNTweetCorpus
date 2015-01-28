DSSNTweetCorpus
===============

Creates a live text corpus from the current (or archived) tweets from twitter.com

Usage
------

In oder to run the Project you need to have the python Twitter-API-Tool from [here](http://mike.verdone.ca/twitter/) and BeautifulSauce from [here](http://www.crummy.com/software/BeautifulSoup/). Furthermore you will need the tokens and consumer keys for the Twitter-Developer-API, which you can get if you ask me.

Current Output
------

Currently the programm will prompt you to insert the screen name of an initial user. All the followers of that user will be inserted into a list. For every user the current timeline (aka latest tweets) will be called, if the user has an unprotected profile. The programm will prompt if he shall gather more users, if so the same method is called again with the next user from the list. Currently a simple HTML/XML file can be created as an output. Though the size is quite high currently and can take time to safe. 

Todo
------

- File output is optional though could be better.
- workaround for following / friending issue.
- maybe provide easy interface if current object format isn't right.
