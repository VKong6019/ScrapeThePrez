import json
import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("./serviceAccountKeys.json")
app = firebase_admin.initialize_app(cred)

database = firestore.client()
candidate_collection = database.collection(u'candidates')


# an attempt to query the database
def query_tweets(keyword, candidate):
    candidate_tweets = candidate_collection.document(candidate).collection("tweets")

    keywordArray = parse_text(keyword)

    # sadly uses multiple queries to search individual words in keyword
    queryArray = []
    for word in keywordArray:
        queryArray.append(candidate_tweets.where(u'keywords', u'array_contains', word).limit(20))

    # return final query list only with complete keyword
    for query in queryArray:
        print(keywordArray)
        print(query.toString)
        if all(elem in keywordArray for elem in queryArray):
            # grabs all tweets with keyword
            for item in query.stream():
                print(item.get('text'))

# text parser to make indexable keywords array
def parse_text(tweet_text):
    text_array = []
    for text in tweet_text.replace(".", "").split():
        text_array.append(text)

    return text_array


query_tweets("skinny", "SenWarren")
