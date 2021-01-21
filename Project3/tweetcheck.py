import tweepy
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from tokens import access_token,access_token_secret,consumer_key,consumer_secret
from country_list import countries


import pandas as pd
import matplotlib.pyplot as plt

from matplotlib import style
style.use('ggplot')

#Basic Listener to print incoming tweets
class StdOutListener(StreamListener):
    def on_data(self,data):
        print(data)
        return True
    
    def on_error(self,status):
        print(status)
        
l = StdOutListener()
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token,access_token_secret)
stream = Stream(auth,l)
api = tweepy.API(auth)
user = api.me()

def fetch_tweets(id,count = 2000):
    tmp = []
    for tweet in tweepy.Cursor(api.user_timeline, id, tweet_mode = "extended").items(count):
        tmp.append(tweet.full_text)
    return tmp

def read_sent_CSV(filename,delimiter = " "):
    df = pd.read_csv(filename)
    full_data = df.values.tolist()
    return full_data

neg_sents = read_sent_CSV('negative_sent.csv')
pos_sents = read_sent_CSV('positive_sent.csv')

def review_sent(tweets,neg_sents,pos_sents):
    ref_countries = {}
    sent_review = {}
    for country in countries:
        sent_c  = 0
        for tweet in tweets:
            if country['name'] in tweet:
                for sent in neg_sents:
                    if sent[0] in tweet:
                        sent_c -=1
                for sent in pos_sents:
                    if sent[0] in tweet:
                        sent_c +=1
                if country['name'] not in sent_review:
                    sent_review[country['name']] = 0
                if country['name'] not in ref_countries:
                    ref_countries[country['name']] = 0
                ref_countries[country['name']]+= 1
                sent_review[country['name']] = sent_c
    return sent_review

def main_app(delegate):
    
    sent_analysis = {}
    tweets = fetch_tweets(delegate,200)
    sent_review = review_sent(tweets,neg_sents,pos_sents)
    sent_analysis[delegate] = sent_review
    
    plt.title(delegate)
    plt.xlabel('countries')
    plt.ylabel('sentiment')
    for country in sent_analysis[delegate]:
        plt.scatter(country,sent_analysis[delegate][country],s=300)
    fig=plt.gcf()
    fig.set_size_inches(20,10)
    plt.savefig('static/images/new_plot.png')

