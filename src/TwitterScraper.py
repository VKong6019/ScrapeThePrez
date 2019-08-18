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


# testing to see if this can scrape some tweets
def get_tweet(input, username):
    page = 1
    deadend = False
    while True:
        tweets = input.user_timeline(username, page=page, include_rts=False, tweet_mode='extended')
        for tweet in tweets:
            if (datetime.datetime.now() - tweet.created_at).days < 2:
                # edit to format for write_to_csv func
                print(tweet.created_at)
                print(tweet.full_text)
                text = tweet.full_text
                write_to_csv(text)
                print("%d times retweeted" % tweet.retweet_count)
            else:
                deadend = True
                return
        if not deadend:
            page += 1
            time.sleep(500)


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
get_tweet(api, "SenWarren")

# write tweets with user-input hashtag phrase to csv file
# hashtag_phrase = raw_input('Hashtag phrase')
