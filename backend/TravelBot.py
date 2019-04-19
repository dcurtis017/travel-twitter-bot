import tweepy, os, json
from decimal import *

import TravelDealDB as tddb
import TwitterHelper
from TravelDealNotifier import send_notification

def process_tweets(event, context):
    twitter_username = TwitterHelper.user.screen_name
    last_tweet_id = tddb.get_user_last_tweet_id(twitter_username)
    if last_tweet_id is None:
        tweets = TwitterHelper.get_initial_tweets()
    else:
        tweets = TwitterHelper.get_tweets(last_tweet_id)
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
    print('Cleaning up tweets older than %s days'%(event['days']))
    tddb.delete_tweets_older_than(event['days'])