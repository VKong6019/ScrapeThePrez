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

# adds tweets to database
def add_to_database(username, tweet_storage):
    for tweet in tweet_storage:
        candidate_collection.document(username).collection('tweets').add({
            'name': tweet.user.screen_name,
            'time': tweet.created_at.__str__(),
            'text': replace_unicode(tweet.full_text),
            'keywords': parse_text(replace_unicode(tweet.full_text))
        })

# text parser to make indexable keywords array
# converts a string into an array of words
def parse_text(tweet_text):
    text_array = []
    for text in tweet_text.replace(".", "").replace('"', '').split():
        text_array.append(text)

    return text_array

# replaces ugly unicode with human-friendly text
def replace_unicode(tweet_text):
    return tweet_text.replace(u"\u2019", "’").replace(u"\u2018", "‘").replace(u"\u2013", "-") \
        .replace(u"\u2014", "—").replace(u"\u2015", "―").replace(u"&amp;", "&")


# scrape the latest tweets given a time and user
def scrape_recent(time, username):
    tweets = api.user_timeline(username, count=200, include_rts=False, tweet_mode='extended')
    new_tweets = []

    for tweet in tweets:
        if compare_time(time, tweet.created_at.__str__):
            new_tweets.append(tweet)
        else:
            break

    add_to_database(username, new_tweets)


# compare two times and return whether the first is older than the second
def compare_time(first_time, second_time):
    first_arr = first_time.replace('-', ' ').replace(':', ' ').split()
    second_arr = second_time.replace('-', ' ').replace(':', ' ').split()

    if first_time == second_time:
        return False

    # checks if all the numbers are bigger or not
    for num in range(len(first_arr)):
        if int(first_arr[num]) > int(second_arr[num]):
            return False

    return True

get_tweet(api, "SenWarren")
get_tweet(api, "SenSanders")

print(compare_time('2019-05-01 16:21:11', '2019-06-01 16:21:11'))
