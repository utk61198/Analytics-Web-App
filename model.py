import re
import tweepy
from textblob import TextBlob





class tweetObject(object):
    api=""
    auth=""


    def __init__(self):

        consumer_key="Pr3cXzpFUDWFoBQeR45uEZuvN"
        consumer_secret="4exOWGmUD1ZVXoCvwOAkafbN6xZlGo7vzrCRpFtb7krYyBc1UP"
        access_token="1138374206750482433-EMwDxdGa9fBSyDlyrcpx9eL1TXxAwN"
        access_token_secret="XSESA9TX8bnoAR53GQCetWm3vZbV4WORV2zGpTEHOLCWj"
        self.auth=tweepy.OAuthHandler(consumer_key,consumer_secret)
        self.auth.set_access_token(access_token,access_token_secret)
        self.api=tweepy.API(self.auth)

        


    def preprocessTweets(self,tweet):
         return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

    def getSentiment(self,tweet):
        analysis=TextBlob(self.preprocessTweets(tweet))
        if analysis.sentiment.polarity > 0:
           return "positive"

        elif analysis.sentiment.polarity == 0:
           return "neutral"
        else:
            return "negative"



    def getTweets(self,topic):
        tweets=[]

        try:
           fetched_tweets=self.api.search(q=topic,tweet_mode='extended')
           for tweet in fetched_tweets:
             polarity = TextBlob(tweet.full_text).sentiment.polarity
             sentiment = TextBlob(tweet.full_text).sentiment.subjectivity
             tweets.append([tweet.full_text,polarity,sentiment])
              
             return tweets
        except tweepy.TweepError as e:
              print("Error:"+str(e))
               






        