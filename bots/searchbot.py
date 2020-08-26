import tweepy
import logging
from config import create_api
import time
from dotenv import load_dotenv, find_dotenv
import os
import pandas as pd
from textblob import TextBlob
import re
import numpy as np
from matplotlib import pyplot as plt
import streamlit as st

load_dotenv(find_dotenv())
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


consumer_key = os.environ.get("CONSUMER_KEY")
consumer_secret = os.environ.get("CONSUMER_SECRET")
access_token = os.environ.get("ACCESS_TOKEN")
access_token_secret = os.environ.get("ACCESS_TOKEN_SECRET")

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth,wait_on_rate_limit=True)

st.title("Twitter Sentiment Analysis")
st.markdown("This is fun :P")

searchtype = st.sidebar.radio(
    "Search by user or text query",
    ('Query', 'Username'))

searchquery = st.sidebar.text_input("Query/Username", "")
searchcount = st.sidebar.slider('# of posts', 0, 100, 30)


def clean_tweet( tweet): 
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split()) 

def get_tweet_sentiment(tweet): 
    ''' 
    Utility function to classify sentiment of passed tweet 
    using textblob's sentiment method 
    '''
    # create TextBlob object of passed tweet text 
    analysis = TextBlob(clean_tweet(tweet)) 
    # set sentiment 
    if analysis.sentiment.polarity > 0: 
        return 'positive'
    elif analysis.sentiment.polarity == 0: 
        return 'neutral'
    else: 
        return 'negative'

if st.sidebar.button('Search'):
    try:
    # Creation of query method using parameters
        if searchtype == 'Query':
            tweets = tweepy.Cursor(api.search,q=searchquery).items(searchcount)
        else: 
            tweets = tweepy.Cursor(api.user_timeline,id=searchquery).items(searchcount)
        # Pulling information from tweets iterable object
        tweets_list = [[clean_tweet(tweet.text), get_tweet_sentiment(tweet.text)]  for tweet in tweets]
        # tweets_slist = [[get_tweet_sentiment(tweet) for tweet in tweets_list]]
        # print(tweets_slist)
        postweets = [tweet for tweet in tweets_list if tweet[1] == 'positive']
        negtweets = [tweet for tweet in tweets_list if tweet[1] == 'negative']
        neutweets = [tweet for tweet in tweets_list if tweet[1] == 'neutral']

        positive = len(postweets)
        negative = len(negtweets)
        neutral = len(neutweets)


        fig = plt.figure()
        labels = ["Positive", "Negative", "Neutral"]
        values = [positive, negative, neutral]
        ax = fig.add_axes([0,0,1,1])
        ax.axis('equal')
        ax.pie(values, labels = labels, autopct='%1.0f%%')
        st.pyplot()
        datatable = pd.DataFrame(tweets_list)
        print(datatable)
        st.table(datatable)
    except BaseException as e:
        print('failed on_status,',str(e))
        time.sleep(3)


