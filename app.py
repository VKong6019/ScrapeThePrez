from flask import Flask, render_template, request
from src.tweet_fetcher import query_tweets

# Flask server for handling HTTP requests
app = Flask(__name__, template_folder="templates")


@app.route('/')
def website():
    return render_template('index.html')


# TODO:
# - Fix 500 HTTP error with app in JS
# - Fix path so that it prints out correctly! (might be solved if we fix first one)
# - make this work for linda time

@app.route('/<path:path>')
def searcher(path):
    result = request.args.get('keywords')
    print(result)
    return result
    results = query_tweets(result, "Danickyflash")
    print(results)
    return render_template('index.html', tweets = results)


if __name__ == '__main__':
    app.run(debug=True)
