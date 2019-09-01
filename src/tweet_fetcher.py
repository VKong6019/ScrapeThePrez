from firebase_admin import credentials, firestore

from src.tweet_scraper import scrape_recent, parse_text

cred = credentials.Certificate("src/./serviceAccountKeys.json")

database = firestore.client()
candidate_collection = database.collection(u'candidates')


# TODO: return an array of json tweets instead of texts
# query the database given a keyword(s) and a candidate
def query_tweets_db(search_term, candidate):
    for doc in candidate_collection.list_documents():
        scrape_recent(candidate_collection.document(doc.id)
                      .collection('last scraped').document('last time').get().get('time'),
                      doc.id)

    candidate_tweets = candidate_collection.document(candidate).collection("tweets")

    keyword_array = parse_text(search_term)

    # sadly uses multiple queries to search individual words in keyword
    for word in keyword_array:
        # multiple queries for multiple words
        query = candidate_tweets.where(u'keywords', u'array_contains', word).limit(20)
        # search all words within iterable query stream
        for item in query.stream():
            # checks if given query has all the keywords
            if all(elem in item.get('keywords') for elem in keyword_array):
                # grabs all tweets with keyword
                return item.get('text')

    print('finito')

# TODO: Make history database index


query_tweets_db('SCRAPE', 'Danickyflash')
