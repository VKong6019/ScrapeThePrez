import os

from flask import Flask, render_template, request, url_for
from src.tweet_scraper import get_tweet

# Flask scrapetheserver for handling HTTP requests
app = Flask(__name__, template_folder="templates")

@app.route('/', methods=['GET', 'POST'])
def website():
    if request.method == 'POST':
        tweet = request.form['keywords']
        # TODO: Make a candidate selector
        return render_template('index.html', tweet=get_tweet(tweet, "Danickyflash"), input=tweet)

    return render_template('index.html')


# TODO:
# - Fix 500 HTTP error with app in JS
# - Fix path so that it prints out correctly! (might be solved if we fix first one)
# - make this work for linda time

if __name__ == '__main__':
    app.run(debug=True)
