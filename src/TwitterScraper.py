import tweepy
import json
import csv
import re
import datetime
import time

from pip._vendor.distlib.compat import raw_input

key_file = open('./secretKeys.json', 'r')
keys = json.loads(key_file.read())

auth = tweepy.OAuthHandler(keys['consumer_key'], keys['consumer_secret'])
auth.set_access_token(keys['access_key'], keys['access_secret'])
api = tweepy.API(auth)


# testing if function can write multiple entries in csv file
# can only scrape a portion of warren's tweets rn
def get_tweet(key, username):
    tweets = key.user_timeline(username, count=200, include_rts=False, tweet_mode='extended')
    tweet_storage = []
    tweet_storage.extend(tweets)
    old = tweet_storage[-1].id - 1

    # pull tweets from the desired Twitter user
    while len(tweets) > 0:
        tweets = key.user_timeline(username, count=200, include_rts=False, tweet_mode='extended', max_id=old)
        tweet_storage.extend(tweets)
        old = tweet_storage[-1].id - 1

    # csv file sorted by columns: name, time, text
    to_csv = [json.dumps({'name': tweet.user.screen_name, 'time': tweet.created_at.__str__(), 'text': tweet.full_text})
              for tweet in tweet_storage]

    # writes into rows as json objects
    with open('tweet_data.csv', 'a') as f:
        to_write = csv.writer(f)
        json_data = [[json.loads(item)['name'], json.loads(item)['time'], json.loads(item)['text'].encode("utf-8")]
                     for item in to_csv]
        to_write.writerows(json_data)
    pass

# we'll use elizabeth warren's acc to test
get_tweet(api, "SenWarren")
get_tweet(api, "SenSanders")
