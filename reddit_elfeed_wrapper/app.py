from functools import wraps
from flask import Flask, make_response
from werkzeug.contrib.atom import AtomFeed
from datetime import datetime as dt
from HTMLParser import HTMLParser
from bs4 import BeautifulSoup
import praw

app = Flask(__name__)

def get_api():
    USER_AGENT = "reddit_wrapper for personalized rss see: /u/kotfic"
    return praw.Reddit(user_agent=USER_AGENT)


def reddit(label, subreddit, limit=25):
    """Decorator used to wrap functions that alter the body of a subreddit
    feed. This function calls out to the subreddit using PRAW and passes the
    decorated function each article object one at a time.  the function is
    expected to return a string containing the desired contents of the atom
    <content> tag."""
    def _reddit(func):
        @wraps(func)
        def wrap_reddit():
            base = "http://www.reddit.com/r/{}/"
            feed = AtomFeed(label,
                            feed_url=base.format(subreddit),
                            url=base.format(subreddit))

            articles = get_api().get_subreddit(subreddit).get_hot(limit=limit)

            for article in articles:
                feed.add(article.title,
                         func(article),
                         content_type='html',
                         author=article.author.name,
                         url=article.url,
                         updated=dt.fromtimestamp(int(article.created)),
                         published=dt.fromtimestamp(int(article.created)))

            r = make_response(feed.get_response())
            r.headers['Content-Type'] = "application/xml"
            return r
        return wrap_reddit
    return _reddit


@app.route('/r/python.atom')
@reddit("Python Subreddit", "python")
def python(article):
    try:
        return HTMLParser().unescape(article.selftext_html)
    except TypeError:
        return ''


@app.route('/r/funny.atom')
@reddit("Funny Subreddit", "funny")
def funny(article):
    try:
        soup = BeautifulSoup("<img src=\"{}\" />".format(article.url))
        return str(soup)
    except TypeError:
        return ''

@app.route('/r/emacs.atom')
@reddit("Emacs Subreddit", "emacs")
def emacs(article):
    try:
        return HTMLParser().unescape(article.selftext_html)
    except TypeError:
        return ''

    

def main():
    app.run(debug=True)


if __name__ == "__main__":
    main()
