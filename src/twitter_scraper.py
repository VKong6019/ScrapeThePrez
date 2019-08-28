import tweepy
import json
import firebase_admin
from firebase_admin import credentials, firestore

# i've got a secret secret
key_file = open('./secretKeys.json', 'r')
keys = json.loads(key_file.read())

cred = credentials.Certificate("./serviceAccountKeys.json")
app = firebase_admin.initialize_app(cred)

auth = tweepy.OAuthHandler(keys['consumer_key'], keys['consumer_secret'])
auth.set_access_token(keys['access_key'], keys['access_secret'])
api = tweepy.API(auth)

# firestore object
database = firestore.client()
candidate_collection = database.collection('candidates')

# it's a surprise tool that will help us later (transactions for doc read/write operations)
tweet_transaction = database.transaction()


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
        # save tweets and update id to oldest tweet
        tweet_storage.extend(tweets)
        old = tweet_storage[-1].id - 1

    # adds each tweet in Firestore as part of the "tweets" collection of respective candidates
    for tweet in tweet_storage:
        candidate_collection.document(username).collection('tweets').add({
            'name': tweet.user.screen_name,
            'time': tweet.created_at.__str__(),
            'text': replace_unicode(tweet.full_text),
            'keywords': parse_text(replace_unicode(tweet.full_text))
        })


# text parser to make indexable keywords array
def parse_text(tweet_text):
    text_array = []
    for text in tweet_text.replace(".", "").split():
        text_array.append(text)

    return text_array


# replaces ugly unicode with human-friendly text
def replace_unicode(tweet_text):
    return tweet_text.replace(u"\u2019", "’").replace(u"\u2018", "‘").replace(u"\u2013", "-") \
        .replace(u"\u2014", "—").replace(u"\u2015", "―").replace(u"&amp;", "&")


# we'll use elizabeth warren's acc to test
get_tweet(api, "SenWarren")
get_tweet(api, "SenSanders")

# get_tweet(input("Search twitter handle: "))
