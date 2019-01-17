from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

import twitter_credential

class MyStreamListener(StreamListener):
    
    def on_data(self, data):
        print(data)
        return True

    def on_error(self, status_code):
        if status_code == 420:
            #returning False in on_data disconnects the stream
            return False



if __name__=="__main__" :

    myStreamListener= MyStreamListener()

auth=OAuthHandler(twitter_credential.Consumer_Key, twitter_credential.Consumer_Key_Secret)
auth.set_access_token(twitter_credential.Access_Token, twitter_credential.Access_Token_Secret)
stream=Stream(auth, myStreamListener)
stream.filter(track=['donald trump'])