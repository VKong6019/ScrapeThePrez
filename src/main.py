import firebase_admin
import csv
import google.cloud

from firebase_admin import credentials, firestore

cred = credentials.Certificate("./serviceAccountKeys.json")
app = firebase_admin.initialize_app(cred)

firestore = firestore.client()

def batch_data(iterable, n=1):
    l = len(iterable)
    for ndx in range(0, l, n):
        yield iterable[ndx:min(ndx + n, l)]

file = "tweet_data.csv"
candidate_tweets = "candidates"

data = []
headers = []
with open(file) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            for header in row:
                headers.append(header)
            line_count += 1
        else:
            obj = {}
            for idx, item in enumerate(row):
                obj[headers[idx]] = item
            data.append(obj)
            line_count += 1
    print(f'Processed {line_count} lines.')

for batched_data in batch_data(data, 200):
    batch = firestore.batch()
    for data_item in batched_data:
        doc_ref = firestore.collection(candidate_tweets).document()
        batch.set(doc_ref, data_item)
    batch.commit()

print('Done')



