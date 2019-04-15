import tweepy, os, json
import TravelDealDB as tddb
from TravelDealNotifier import send_notification

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
airport_dict = {'atl': 'Atlanta', 'clt': 'Charlotte', 'rdu': 'Raleigh'}
user = api.me()
print('Populating flight deals for', user.screen_name)

def get_list_members():
    members = []
    for page in tweepy.Cursor(api.list_members, user.screen_name, list_name).items():
        members.append(page)
    return [m.screen_name for m in members]

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
                map(lambda: x: airport_dict[x.lower()] if x.lower() in airport_dict else x, kws)
            )
            caps_on = [x.capitalize() for x in formatted_kws]
            deduped = list(dict.fromkeys(caps_on))
            deduped.sort()
            relevant_tweets.append({'text': tweet.text, 'tweet_id': int(tweet.id_str), 'created_at': tweet.created_at.isoformat(), 'screen_name': tweet.user.screen_name, 'search_terms': '-'.join(deduped)})
    return relevant_tweets

def process_tweets(event, context):
    twitter_username = user.screen_name
    last_tweet_id = tddb.get_user_last_tweet_id(twitter_username)
    if last_tweet_id is None:
        tweets = get_initial_tweets()
    else:
        tweets = get_tweets(last_tweet_id)
    if len(tweets) > 0:
        print('Saving %d tweets'%len(tweets))
        tddb.insert_tweets(tweets)
        update_twitter_user(twitter_username, tweets[0]['tweet_id'], last_tweet_id is not None)
        send_notification(twitter_username, len(tweets))
    else:
        print('No new tweets :(')

def update_twitter_user(twitter_username, last_tweet_id, user_exists):
    user = {
        'twitter_username': twitter_username,
        'last_tweet_id': last_tweet_id
    }
    if user_exists:
        response = tddb.update_user(user)
    else:
        response = tddb.insert_user(user)

def process_tweet_cleanup(event, context):
    members = get_list_members()
    print('Cleaning up tweets older than %s days'%(event['days']))
    tddb.delete_tweets_older_than(members, event['days'])

def get_airports(event, context):
    return {
       "statusCode": 200,
       "body": list(airport_dict.values())
    }

def get_twitter_list_members(event, context):
    return {
        "statusCode": 200,
        "body": get_list_members()
    }

def get_airport_tweets(event, context):
    print(event)
    #pass airport code