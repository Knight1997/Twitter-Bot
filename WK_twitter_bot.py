# -*- coding: utf-8 -*-
"""
Created on Tue Dec 18 06:28:59 2018

@author: Dell
"""

import tweepy
import time

CONSUMER_KEY=''
CONSUMER_SECRET=''
ACCESS_KEY=''
ACCESS_SECRET=''

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api=tweepy.API(auth)

#saving ids in a file to resolve redundant replying
FILE_NAME='Last_seen_ids.txt'

def get_last_seen_id(file_name):
    f_read = open(file_name,'r')
    last_seen_id=int(f_read.read().strip())
    f_read.close();
    return last_seen_id

def store_last_seen_id(last_seen_id, file_name):
    f_write=open(file_name,'w')
    f_write.write(str(last_seen_id))
    f_write.close()
    return

def reply_tweets():
    print('Retriving and replying to tweets!!')
    last_seen_id=get_last_seen_id(FILE_NAME)
    mentions=api.mentions_timeline(last_seen_id, tweet_mode='extended')
    
    for mention in reversed(mentions):
        print(str(mention.id)+' --> '+ mention.full_text)
        last_seen_id = mention.id
        store_last_seen_id(last_seen_id,FILE_NAME)
        if '#helloworld' in mention.full_text.lower():
            api.update_status('@' + mention.user.screen_name + ' Build you own castle! ', mention.id)
    
while(True):
    reply_tweets()
    time.sleep(15)
    

