import cgi
import cgitb

import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("./serviceAccountKeys.json")
app = firebase_admin.initialize_app(cred)

database = firestore.client()
candidate_collection = database.collection(u'candidates')

# connects searchbar to CGI
cgitb.enable()
search_form = cgi.FieldStorage()

keyword = search_form.getvalue('keywords')

# an attempt to query the database
def query_tweets(keyword, candidate):
    candidate_tweets = candidate_collection.document(candidate).collection("tweets")

    keywordArray = parse_text(keyword)
    print(keywordArray)

    # sadly uses multiple queries to search individual words in keyword
    for word in keywordArray:
        # multiple queries for multiple words
        query = candidate_tweets.where(u'keywords', u'array_contains', word).limit(20)
        # search all words within iterable query stream
        for item in query.stream():
            print(keywordArray)
            print(item.get('keywords'))
            # checks if given query has all the keywords
            if all(elem in item.get('keywords') for elem in keywordArray):
                # grabs all tweets with keyword
                print(item.get('text'))


# text parser to make indexable keywords array
def parse_text(tweet_text):
    text_array = []
    for text in tweet_text.replace(".", "").split():
        text_array.append(text)

    return text_array


# Display results on website
print('Content-Type:text/html\n')
print("<h1>Results</h1>")
query_tweets(keyword, "SenWarren")

# query_tweets("More than 2000", "SenWarren")
# query_tweets('Puerto', "SenSanders")
