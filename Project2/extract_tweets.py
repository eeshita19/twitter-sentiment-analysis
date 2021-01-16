from tweepy import Cursor
from tweepy import API
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import tokens

from textblob import TextBlob
import re 

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time
import json
import os


# # # Authentication # # #
class TwitterAuthentication():
    
    def authenticate_twitter_app(self):
        auth = OAuthHandler(tokens.consumer_key,tokens.consumer_secret)
        auth.set_access_token(tokens.access_token,tokens.access_token_secret)
        return auth


class TwitterListener(StreamListener):
    """
    Listener class
    """
    
    
    def __init__(self, fetched_tweets_file,time_limit=60):
        self.fetched_tweets_file = fetched_tweets_file
        self.start_time = time.time()
        self.limit = time_limit

    def on_data(self,data):
        
        try:
            if not os.path.exists(fetched_tweets_file):
                with open(self.fetched_tweets_file,'a') as tf:
                    tf.write("[")
                    tf.write(data)
                    
            else:                
                with open(self.fetched_tweets_file,'a') as tf:
                    if (time.time() - self.start_time) < self.limit:
                
                        tf.write(",")
                        tf.write(data)                        
                        return True
                    else:
                        tf.write("]")
                        return False
        except BaseException as e:
            print("Error on data: " + str(e))
        return True

    def on_error(self,status):
        if status == 420:
            return False
        print(status)

class TwitterStreamer():
    """
    processing tweets 
    """
    
    def __init__(self):
        self.twitter_authenticator = TwitterAuthentication()

    def stream_tweets(self, fetched_tweets_file, hashtag_list,count=20):
        TwitterListener.stopAt = count
        
        listener = TwitterListener(fetched_tweets_file,time_limit=20)
        auth = self.twitter_authenticator.authenticate_twitter_app()        

        stream = Stream(auth,listener)
        stream.filter(track=hashtag_list)




class TweetAnalyzer():
    """
    functionality for analyzing tweets
    """
    def clean_tweets(self, tweet):
        tw = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \\t])|(\\w+:\\/\\/\\S+)", '', str(tweet)).split())
        return tw
        
    def analyze_sent(self, tweet):
        analysis = TextBlob(self.clean_tweets(tweet))
        return analysis.sentiment.polarity 
            
    
    def tweets_to_df(self,tweets):
        df = pd.DataFrame(data=[tweet["text"] for tweet in tweets], columns=['tweets'])
        
        df['id'] = np.array([tweet["id"] for tweet in tweets])
        df['len'] = np.array([len(tweet["text"]) for tweet in tweets])
        df['date'] = np.array([tweet["created_at"] for tweet in tweets])
        df['source'] = np.array([tweet["source"] for tweet in tweets])
        df['likes'] = np.array([tweet["favorite_count"] for tweet in tweets])
        df['retweet'] = np.array([tweet["retweet_count"] for tweet in tweets])
        
        return df



if __name__ == "__main__":
    
    tweetanalyze = TweetAnalyzer()
    fetched_tweets_file = "tweets.json"
    '''
    twitterstream = TwitterStreamer() 
    
    hashtag_list = ["selena gomez","barack obama", "hillary clinton", "narendra modi"]
    
    twitterstream.stream_tweets(fetched_tweets_file,hashtag_list,5)
    '''
    
    with open(fetched_tweets_file) as complex_data:
        data = complex_data.read()
        tweets = json.loads(data)

    #print(type(tweets))
    
    df = tweetanalyze.tweets_to_df(tweets)
    
    df['sent'] = np.array([tweetanalyze.analyze_sent(tweet["text"]) for tweet in tweets])
    print(df.head())
    
    
    