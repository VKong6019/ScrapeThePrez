import cgi
import cgitb

import firebase_admin
from firebase_admin import credentials, firestore
from flask import Flask, render_template, request

cred = credentials.Certificate("./serviceAccountKeys.json")
app = firebase_admin.initialize_app(cred)

database = firestore.client()
candidate_collection = database.collection(u'candidates')

web_server = Flask(__name__)


@web_server.route('/')
def website():
    return render_template('index.html')


@web_server.route('/result', methods=['POST', 'GET'])
def result():
    if request.method == 'POST':
        result = request.form['keywords']
        print(result)
        return "success"


if __name__ == '__main__':
    web_server.run(debug=True)


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


def search_form():
    # connects searchbar to CGI
    cgitb.enable()
    search_form = cgi.FieldStorage()

    keyword = search_form.getvalue('keywords')
    # Display results on website
    print('Content-Type:text/html\n')
    print("<h1>Results</h1>")
    print("<FORM method='post' method='tweet_fetcher.py'")
    query_tweets(keyword, "SenWarren")

# query_tweets("More than 2000", "SenWarren")
# query_tweets('Puerto', "SenSanders")
