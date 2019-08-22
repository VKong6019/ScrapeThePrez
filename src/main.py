import firebase_admin
import csv
import google.cloud

from firebase_admin import credentials, firestore

cred = credentials.Certificate("./serviceAccountKeys.json")
app = firebase_admin.initialize_app(cred)

firestore = firestore.client()

# batches data into bulks
def batch_data(iterable, n=1):
    l = len(iterable)
    for ndx in range(0, l, n):
        yield iterable[ndx:min(ndx + n, l)]

file = "fake_data.csv"
candidate_tweets = "candidates"

data = []
headers = []

# reads and parses csv file
with open(file) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
    # case for recording column labels - organization
        headers.append("name")
        headers.append("time")
        headers.append("text")
        obj = {}
        for idx, item in enumerate(row):
            obj[headers[idx]] = item
        data.append(obj)
        line_count += 1
    print(f'Processed {line_count} lines.')

# writes all data into Cloud Firestone
for batched_data in batch_data(data, 10):
    batch = firestore.batch()
    for data_item in batched_data:
        doc_ref = firestore.collection(candidate_tweets).document()
        batch.set(doc_ref, data_item)
    batch.commit()

print('Done')



