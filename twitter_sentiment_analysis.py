from tweepy import API 
from tweepy import Cursor
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
 
import twitter_credentials
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#for Sentiment Analysis
from textblob import TextBlob
import re #Regular Expression

# # # # TWITTER CLIENT # # # #
class TwitterClient():
    def __init__(self, twitter_user=None):
        self.auth = TwitterAuthenticator().authenticate_twitter_app()
        self.twitter_client = API(self.auth)

        self.twitter_user = twitter_user

    def get_user_timeline_tweets(self, num_tweets):
        tweets = []
        for tweet in Cursor(self.twitter_client.user_timeline, id=self.twitter_user).items(num_tweets):
            tweets.append(tweet)
        return tweets

    def get_friend_list(self, num_friends):
        friend_list = []
        for friend in Cursor(self.twitter_client.friends, id=self.twitter_user).items(num_friends):
            friend_list.append(friend)
        return friend_list

    def get_home_timeline_tweets(self, num_tweets):
        home_timeline_tweets = []
        for tweet in Cursor(self.twitter_client.home_timeline, id=self.twitter_user).items(num_tweets):
            home_timeline_tweets.append(tweet)
        return home_timeline_tweets


# # # # TWITTER AUTHENTICATER # # # #
class TwitterAuthenticator():

    def authenticate_twitter_app(self):
        auth = OAuthHandler(twitter_credentials.CONSUMER_KEY, twitter_credentials.CONSUMER_SECRET)
        auth.set_access_token(twitter_credentials.ACCESS_KEY, twitter_credentials.ACCESS_SECRET)
        return auth

# # # # TWITTER STREAMER # # # #
class TwitterStreamer():
    """
    Class for streaming and processing live tweets.
    """
    def __init__(self):
        self.twitter_autenticator = TwitterAuthenticator()    

    def stream_tweets(self, fetched_tweets_filename, hash_tag_list):
        # This handles Twitter authetification and the connection to Twitter Streaming API
        listener = TwitterListener(fetched_tweets_filename)
        auth = self.twitter_autenticator.authenticate_twitter_app() 
        stream = Stream(auth, listener)

        # This line filter Twitter Streams to capture data by the keywords: 
        stream.filter(track=hash_tag_list)


# # # # TWITTER STREAM LISTENER # # # #
class TwitterListener(StreamListener):
    """
    This is a basic listener that just prints received tweets to stdout.
    """
    def __init__(self, fetched_tweets_filename):
        self.fetched_tweets_filename = fetched_tweets_filename

    def on_data(self, data):
        try:
            print(data)
            with open(self.fetched_tweets_filename, 'a') as tf:
                tf.write(data)
            return True
        except BaseException as e:
            print("Error on_data %s" % str(e))
        return True
          
    def on_error(self, status):
        if status == 420:
            # Returning False on_data method in case rate limit occurs.
            return False
        print(status)

class TweetAnalyzer():
    """
    Functionality for analyzing and categorizing content from tweets.
    """
    #Regular Expression is used for cleaning
    def clean_tweet(self, tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

    def analyze_sentiment(self, tweet):
        analysis = TextBlob(self.clean_tweet(tweet))
        
        if analysis.sentiment.polarity > 0:
            return 1000
        elif analysis.sentiment.polarity == 0:
            return 0
        else:
            return -1000
    
    def perform_sentiment_analysis(self,df):
        return np.array([self.analyze_sentiment(tweet.text) for tweet in tweets])

    def tweets_to_data_frame(self, tweets):
        df = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['tweets'])

        df['id'] = np.array([tweet.id for tweet in tweets])
        df['len'] = np.array([len(tweet.text) for tweet in tweets])
        df['date'] = np.array([tweet.created_at for tweet in tweets])
        df['source'] = np.array([tweet.source for tweet in tweets])
        df['likes'] = np.array([tweet.favorite_count for tweet in tweets])
        df['retweets'] = np.array([tweet.retweet_count for tweet in tweets])
        df['sentiment']=self.perform_sentiment_analysis(df)
        return df

class Visualizer():
    """
        plotting the graph bwtween likes,retweets and date 
    """
    def visualizing_likes_and_retweets(self, df):
        # Layered Time Series:
        time_likes = pd.Series(data=df['likes'].values, index=df['date'])
        time_likes.plot(figsize=(16, 4), label="likes", legend=True)
    
        time_retweets = pd.Series(data=df['retweets'].values, index=df['date'])
        time_retweets.plot(figsize=(16, 4), label="retweets", legend=True)
        
        
        time_retweets = pd.Series(data=df['sentiment'].values, index=df['date'])
        time_retweets.plot(figsize=(16, 4), label="retweets", legend=True)
        plt.show()
        
if __name__ == '__main__':
 
    # Authenticate using config.py and connect to Twitter Streaming API.
    hash_tag_list = ["BJP","Narendra Modi","Modi","Bhartyia janta party"]
    fetched_tweets_filename = "tweets.txt"

    user_handle="sambitswaraj"
    twitter_client = TwitterClient(user_handle)
    tweets=twitter_client.get_user_timeline_tweets(100)
    
    tweet_analyzer=TweetAnalyzer()
    df=tweet_analyzer.tweets_to_data_frame(tweets)
    
    visualizer=Visualizer()
    visualizer.visualizing_likes_and_retweets(df)
    
    print(df.head(10))
    
    

#    twitter_streamer = TwitterStreamer()
#    twitter_streamer.stream_tweets(fetched_tweets_filename, hash_tag_list)