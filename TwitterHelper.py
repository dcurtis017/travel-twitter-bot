import tweepy, os

from Airports import *

# credentials
consumer_key = os.environ['TWITTER_CONSUMER_KEY']
consumer_secret = os.environ['TWITTER_CONSUMER_SECRET']
access_token = os.environ['TWITTER_ACCESS_TOKEN']
access_token_secret = os.environ['TWITTER_ACCESS_TOKEN_SECRET']

# authenticate
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

list_name = 'flight-deals'

user = api.me()

def get_list_members():
    members = []
    for page in tweepy.Cursor(api.list_members, user.screen_name, list_name).items():
        members.append(page)
    return [{'screen_name': m.screen_name, 'display_name': m.name} for m in members]

def get_initial_tweets():
    tweets = []
    for page in tweepy.Cursor(api.list_timeline, user.screen_name, list_name, page=1).items():
        tweets.append(page)
    return get_relevant_tweets(tweets)

def get_tweets(last_tweet_id):
    tweets = []
    for page in tweepy.Cursor(api.list_timeline, user.screen_name, list_name, since_id=last_tweet_id).items():
        tweets.append(page)
    return get_relevant_tweets(tweets)

def get_relevant_tweets(tweets):
    relevant_tweets = []
    for tweet in tweets:
        tweet_text = tweet.text.lower()
        if any(kw in tweet_text for kw in my_keywords):
            # figure out which keywords
            kws = [my_keywords[ind] for ind, kw in enumerate(my_keywords) if kw in tweet_text]
            formatted_kws = list(
                map(lambda x: airport_dict[x.lower()] if x.lower() in airport_dict else x, kws)
            )
            caps_on = [x.capitalize() for x in formatted_kws]
            deduped = list(dict.fromkeys(caps_on))
            deduped.sort()
            for d in deduped:
                relevant_tweets.append({'text': tweet.text, 'tweet_id': int(tweet.id_str), 'created_at': tweet.created_at.isoformat(), 'screen_name': tweet.user.screen_name, 'search_terms': d})
    return relevant_tweets