# import tweepy
# import datetime, time
import json

key_file = open('./secretKeys.json', 'r')
keys = json.loads(key_file.read())

print(keys['consumer_key'])

# auth = tweepy.OAuthHandler(keys['consumer_key'], 'consumer_secret')
# auth.set_access_token('access_key', 'access_secret')
# api = tweepy.API(auth)


# # testing to see if this can scrape some tweets
# def get_tweet(input, username):
#     page = 1
#     deadend = False
#     while True:
#         tweets = input.user_timeline(username, page=page)
#         for tweet in tweets:
#             if (datetime.datetime.now() - tweet.created_at).days < 2:
#                 print(tweet.text.encode("utf-8"))
#             else:
#                 deadend = True
#                 return
#         if not deadend:
#             page + 1
#             time.sleep(500)

# # we'll use elizabeth warren's acc to test
# get_tweet(api, "SenWarren")

