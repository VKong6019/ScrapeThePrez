import cgi
import cgitb

import firebase_admin
from firebase_admin import credentials, firestore

from src.tweet_scraper import scrape_recent

cred = credentials.Certificate("./serviceAccountKeys.json")

database = firestore.client()
candidate_collection = database.collection(u'candidates')

# connects searchbar to CGI
cgitb.enable()
search_form = cgi.FieldStorage()

keyword = search_form.getvalue('keywords')
print(keyword)
print("Content-type:text/html\r\n\r\n")
print("<html>")
print("<head>")
print("<title>Hello - Second CGI Program</title>")
print("</head>")
print("<body>")
print("<h2>Hello there</h2>")
print("</body>")
print("</html>")

# # an attempt to query the database
# def query_tweets(search_term, candidate):
#     for doc in candidate_collection.list_documents():
#         scrape_recent(candidate_collection.document(doc.id)
#                       .collection('last scraped').document('last time').get().get('time'),
#                       doc.id)
#
#     candidate_tweets = candidate_collection.document(candidate).collection("tweets")
#
#     keyword_array = parse_text(search_term)
#     print(keyword_array)
#
#     # sadly uses multiple queries to search individual words in keyword
#     for word in keyword_array:
#         # multiple queries for multiple words
#         query = candidate_tweets.where(u'keywords', u'array_contains', word).limit(20)
#         # search all words within iterable query stream
#         for item in query.stream():
#             print(keyword_array)
#             print(item.get('keywords'))
#             # checks if given query has all the keywords
#             if all(elem in item.get('keywords') for elem in keyword_array):
#                 # grabs all tweets with keyword
#                 print(item.get('text'))
#
#
# # text parser to make indexable keywords array
# def parse_text(tweet_text):
#     text_array = []
#     for text in tweet_text.replace(".", "").split():
#         text_array.append(text)
#
#     return text_array
#
#
# # Display results on website
# print('Content-Type:text/html\n')
# print("<h1>Results</h1>")
# query_tweets('trump', "ewarren")

