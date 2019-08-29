from flask import Flask, render_template, request
# from tweet_fetcher import query_tweets

# Flask server for handling HTTP requests
app = Flask(__name__, template_folder="templates")


@app.route('/')
def website():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def searcher():
    result = request.form['keywords']
    # tweets = query_tweets(result, "ewarren")
    print(result)
    # return render_template('index.html', tweets = tweets)


if __name__ == '__main__':
    app.run(debug=True)
