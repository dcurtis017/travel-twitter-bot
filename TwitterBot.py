import tweepy, os

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
my_keywords = ['clt', 'rdu', 'atl', 'charlotte', 'raleigh', 'atlanta']
user = api.me()

def get_list_members():    
    members = []
    for page in tweepy.Cursor(api.list_members, user.screen_name, list_name).items():
        members.append(page)
    return [m.screen_name for m in members]

# 1109870060020137984
def get_tweets(last_tweet_id):
    tweets = []
    for page in tweepy.Cursor(api.list_timeline, user.screen_name, list_name, since_id=last_tweet_id, page=1).items():
        tweets.append(page)

    relevant_tweets = []
    for tweet in tweets:
        tweet_text = tweet.text.lower()
        if any(kw in tweet_text for kw in my_keywords):
            # figure out which keywords
            kws = [my_keywords[ind] for ind, kw in enumerate(my_keywords) if kw in tweet_text]
            relevant_tweets.append({'text': tweet.text, 'id': tweet.id_str, 'created_at': tweet.created_at, 'screen_name': tweet.user.screen_name, 'kw_matches': '-'.join([k.upper() for k in kws])})
    return relevant_tweets

       
