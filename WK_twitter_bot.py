# -*- coding: utf-8 -*-
"""
Created on Tue Dec 18 06:28:59 2018

@author: Dell
"""

import tweepy

CONSUMER_KEY='ysvqCFn7aEEpR6W8fNePMRxoK '
CONSUMER_SECRET='NOg27fr7BHw2ZCbbsnyCTPp0zmjk16rk9C0w1MJGAfqVvMURXq '
ACCESS_KEY='223796937-DLIS14oo7dYXWUF2ondgAEYk1NL4F5GrcsiFSa3A'
ACCESS_SECRET='HxElCbiak72rz8xwxLhD52xuCURXbzfbJuJIMyKjNVoJ7 '

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api=tweepy.API(auth)


