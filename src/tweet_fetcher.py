import json
import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("./serviceAccountKeys.json")
app = firebase_admin.initialize_app(cred)

database = firestore.client()
candidate_collection = database.collection(u'candidates')


# an attempt to query the database
def query_tweets(text):
    query = candidate_collection.where(u'keywords', u'array_contains', text).limit(20)

    for item in query.stream():
        print(json.loads(item)['text'])
