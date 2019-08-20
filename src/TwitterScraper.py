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
    while len(tweets) > 0:
        tweets = key.user_timeline(username, count=200, include_rts=False, tweet_mode='extended', max_id=old)
        tweet_storage.extend(tweets)
        old = tweet_storage[-1].id - 1

    to_csv = [json.dumps({'name': tweet.user.screen_name, 'time': tweet.created_at.__str__(), 'text': tweet.full_text})
              for tweet in tweet_storage]

    with open('tweet_data.csv', 'w') as f:
        to_write = csv.writer(f)
        json_data = [[json.loads(item)['name'], json.loads(item)['time'], json.loads(item)['text'].encode("utf-8")]
                     for item in to_csv]
        to_write.writerows(json_data)
    pass


# update and upgrade this so that:
# - columns for different fields
# - grouped by twitter handle
# - more than one tweet (TURTLES)

def write_to_csv(text):
    # open spreadsheet
    tweet_data = open('tweet_data.csv', 'w')
    with tweet_data as file:
        tweet_data.write(text)

    # we'll use elizabeth warren's acc to test
    get_tweet(api, "SenWarren")

    # file = '_'.join(re.findall(r"#(\w+)", hashtag_phrase))
    #
    # # open spreadsheet
    # with open('%s.csv' % (file), 'wb') as file:
    #     w = csv.writer(file)
    #     # write header row to spreadsheet
    #     w.writerow(['timestamp', 'tweet_text', 'username', 'all_hashtags'])
    #
    #     # for each tweet matching our hashtags, write relevant info to spreadsheet
    #     for tweet in tweepy.Cursor(api.search, q=hashtag_phrase + ' -filter:retweets',
    #                                lang="en", tweet_mode='extended').items(100):
    #         w.writerow([tweet.created_at, tweet.full_text.replace('\n', ' ').encode('utf-8'),
    #                     tweet.user.screen_name.encode('utf-8'),
    #                     [e['text'] for e in tweet.json['entities']['hashtags']]])


# we'll use elizabeth warren's acc to test
get_tweet(api, "ewarren")

# write tweets with user-input hashtag phrase to csv file
# hashtag_phrase = raw_input('Hashtag phrase')
