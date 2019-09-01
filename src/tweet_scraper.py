import tweepy
import json
import firebase_admin
import datetime
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

# list of all candidates
republicans = ["Donald J. Trump", "Joe Walsh", "William F. Weld"]
republicans_handles = ["realDonaldTrump", "WalshFreedom", "GovBillWeld"]
republicans_websites = ["https://www.donaldjtrump.com", "https://www.joewalsh.org", "https://www.weld2020.org"]

democrats = ["Michael Bennet", "Joseph R. Biden Jr.", "Cory Booker", "Steve Bullock", "Pete Buttigieg", "Julián Castro",
             "Bill de Blasio", "John Delaney", "Tulsi Gabbard", "Kamala Harris", "Amy Klobuchar", "Wayne Messam",
             "Beto O'Rourke", "Tim Ryan", "Bernie Sanders", "Joe Sestak", "Tom Steyer", "Elizabeth Warren",
             "Marianne Williamson", "Andrew Yang"]
democrats_handles = ["MichaelBennet", "JoeBiden", "CoryBooker", "GovernorBullock", "PeteButtigieg", "JulianCastro",
                     "BilldeBlasio", "TulsiGabbard", "KamalaHarris", "amyklobuchar", "WayneMessam", "BetoORourke",
                     "TimRyan", "SenSanders", "JoeSestak", "TomSteyer", "ewarren", "marwilliamson", "AndrewYang"]
democrats_websites = ["https://www.michaelbennet.com", "https://www.joebiden.com", "https://www.corybooker.com",
                      "https://www.stevebullock.com", "https://www.peteforamerica.com",
                      "https://www.julianforthefuture.com", "https://www.billdeblasio.com",
                      "https://www.johndelaney.com", "https://www.tulsi2020.com", "https://www.kamalaharris.org",
                      "https://www.amyklobuchar.com", "https://www.WayneForUSA.com", "https://www.betoorourke.com",
                      "https://www.timryanforamerica.com", "https://www.berniesanders.com", "https://www.joesestak.com",
                      "https://www.tomsteyer.com", "https://www.elizabethwarren.com", "https://www.marianne2020.com",
                      "https://www.yang2020.com"]

keyword_tweets = []


# searches tweets from desired candidates based on keyword
def get_tweet(keyword, username):
    tweets = api.user_timeline(username, count=200, include_rts=False, tweet_mode='extended')

    # store all tweets from username in array
    tweet_storage = []
    tweet_storage.extend(tweets)

    keyword_tweets = []
    for tweet in tweet_storage:
        # if keyword is found in the tweet text, add to array of tweets with keyword
        if replace_unicode(tweet.full_text).find(keyword) != -1:
            print(tweet.full_text)
            keyword_tweet = json.dumps({'name': tweet.user.screen_name,
                                        'time': tweet.created_at.__str__(),
                                        'text': replace_unicode(tweet.full_text)})
            keyword_tweets.append(keyword_tweet)
    print(keyword_tweets)


# testing if function can write multiple entries
def get_tweet_db(username):
    tweets = api.user_timeline(username, count=200, include_rts=False, tweet_mode='extended')
    tweet_storage = []
    tweet_storage.extend(tweets)
    old = tweet_storage[-1].id - 1

    # pull tweets from the desired Twitter user
    while len(tweets) > 0:
        tweets = api.user_timeline(username, count=200, include_rts=False, tweet_mode='extended', max_id=old)
        # save tweets and update id to oldest tweet
        tweet_storage.extend(tweets)
        old = tweet_storage[-1].id - 1

    add_to_database(username, tweet_storage)


# adds tweets to database
def add_to_database(username, tweet_storage):
    for tweet in tweet_storage:
        candidate_collection.document(username).collection('tweets').add({
            'name': tweet.user.screen_name,
            'time': tweet.created_at.__str__(),
            'text': replace_unicode(tweet.full_text),
            'keywords': parse_text(replace_unicode(tweet.full_text))
        })

    if len(tweet_storage) > 0:
        candidate_collection.document(username).collection('last scraped').document('last time').set({
            'time': tweet_storage[0].created_at.__str__()
        })


# text parser to make indexable keywords array
# converts a string into an array of words, lowercased
def parse_text(tweet_text):
    text_array = []
    for text in tweet_text.replace(".", "").replace('"', '').split():
        text_array.append(text.lower())

    return text_array


# replaces ugly unicode with human-friendly text
def replace_unicode(tweet_text):
    return tweet_text.replace(u"\u2019", "’").replace(u"\u2018", "‘").replace(u"\u2013", "-") \
        .replace(u"\u2014", "—").replace(u"\u2015", "―").replace(u"&amp;", "&")


# scrape the latest tweets given a time and user
def scrape_recent(time, username):
    tweets = api.user_timeline(username, count=20, include_rts=False, tweet_mode='extended')
    new_tweets = []

    for tweet in tweets:
        if compare_time(time, tweet.created_at.__str__()):
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

    if datetime.date(int(first_arr[0]), int(first_arr[1]), int(first_arr[2])) \
            > datetime.date(int(second_arr[0]), int(second_arr[1]), int(second_arr[2])):
        return False
    elif datetime.date(int(first_arr[0]), int(first_arr[1]), int(first_arr[2])) \
            == datetime.date(int(second_arr[0]), int(second_arr[1]), int(second_arr[2])):
        return convert_to_sec(first_arr[3], first_arr[4], first_arr[5]) \
               > convert_to_sec(second_arr[3], second_arr[4], second_arr[5])

    return True


def convert_to_sec(hour, minute, sec):
    return int(hour) * 3600 + int(minute) * 60 + int(sec)


get_tweet("@pavster2017", "Danickyflash")
print('finito')
