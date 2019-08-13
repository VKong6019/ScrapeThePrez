import tweepy
import datetime, time

auth = tweepy.OAuthHandler("vJKlXHvf9oOmzeKPwDARmfxSV", "qrPSw7Gw65lv2V4KWWEhuKDpUPfVMinaGx7aIfzJ7Qie7K5DLH")
auth.set_access_token("913178822-dycOPGPAGmGoeoZNFH4Jo6SV1tIJqClPMbv9h1MD",
                      "44P7aFLvqWXrbXmFBzfJ1KPFCnef5PoCtKXtiLLjmerbh")
api = tweepy.API(auth)


# testing to see if this can scrape some tweets
def get_tweet(input, username):
    page = 1
    deadend = False
    while True:
        tweets = input.user_timeline(username, page=page)
        for tweet in tweets:
            if (datetime.datetime.now() - tweet.created_at).days < 2:
                print(tweet.text.encode("utf-8"))
            else:
                deadend = True
                return
        if not deadend:
            page + 1
            time.sleep(500)

# we'll use elizabeth warren's acc to test
get_tweet(api, "SenWarren")

