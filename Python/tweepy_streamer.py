#Importing tweepy classes.

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import twitter_credential
#Creating MyStreamListenerclass
class TweetStreamer():
       
    def __init__(self):
        pass
    
    
    def stream_tweets(self, fetched_tweets_filename, search_param):
        #Adding credentials, referencing twitter_credential file.
            myStreamListener= MyStreamListener(fetched_tweets_filename)
            auth=OAuthHandler(twitter_credential.Consumer_Key, twitter_credential.Consumer_Key_Secret)
            auth.set_access_token(twitter_credential.Access_Token, twitter_credential.Access_Token_Secret)
            stream=Stream(auth, myStreamListener)
#Function to search for a tweet having particular word. For example: Donald trump.
            stream.filter(track=search_param)



class MyStreamListener(StreamListener):
    
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
        print(status)



#Main method.

if __name__=="__main__" :
    names=input("Enter keyword to be searched:")
    search_param= [names]    
    fetched_tweets_filename= "Tweets.json"
    twitter_streamer = TweetStreamer()
    twitter_streamer.stream_tweets(fetched_tweets_filename, search_param)
