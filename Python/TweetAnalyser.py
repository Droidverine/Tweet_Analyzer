#!/usr/bin/env python
# coding: utf-8

# In[5]:



access_token="448140491-9geQ6MbH0voyY9jPYp51jaTYj0m4b5L25rPLI0ly"
access_token_secret="owBK4P7Um0szSkKVt1jR89VBcCOSHlbqaiAKRg8080jj5"
consumer_key="DZIF3QS3wf8pYC7mZr6zGdKkM"
consumer_key_secret="fi0fR2GPZNO4ex2g83coD6kinTzu5OPBaNgGIMO5uFWOEMYqSw"


# In[44]:


#!pip3 install tweepy
import tweepy
import textblob as tb
import json
import numpy as np
import pandas as pd
import matplotlib as plt

auth = tweepy.OAuthHandler(consumer_key, consumer_key_secret)
auth.set_access_token(access_token, access_token_secret)


# In[13]:


#Searching tweets here

api = tweepy.API(auth)
names=input("Enter keyword to be searched:")
search_param= [names]    
#public_tweets = api.home_timeline()
x = api.search(q=names
               ,locale='English'
               ,count = 200)
c = 0
for tweet in x:
    print("'",tweet.text,"'",",")
    c += 1


# In[30]:


tweetbase = open('tweets.txt','w')
#inputString.encode('ascii', 'ignore').decode('ascii')

for tweet in x:
    print(str(tweet.text).encode('ascii', 'ignore').decode('ascii'))
    tweetbase.write(str(tweet.text).encode('ascii', 'ignore').decode('ascii'))
    #tweetbase.write('\n\n,\n\n')
tweetbase.close()


# In[31]:


dataset = open('tweets.txt','r')
data_list = []
for line in dataset:
    data_list.append(line)
print(data_list)


# In[48]:


polarity=[]
for i in range(0,len(data_list)):
    testimonial = tb.TextBlob(data_list[i])
    print(#testimonial.tags,
          '\n\n',
          i,
          #data_list[i],
          testimonial.sentiment,
          '\n\n')
    polarity.append(testimonial.sentiment.polarity)


# In[53]:


#Matplotlib
print(polarity)
np.random.seed(22321421)


plt.rcdefaults()
fig, ax = plt.pyplot.subplots()


# Example data
y_pos = np.arange(len(data_list))

ax.barh(y_pos, align='center',
        color='green', ecolor='black',width = 1)
ax.set_yticks(y_pos)
ax.set_yticklabels(range(1,len(data_list)))
ax.invert_yaxis()  # labels read top-to-bottom
ax.set_xlabel('Polarity')
ax.set_title('Polarity relationship')

plt.pyplot.show()

