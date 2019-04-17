import tweepy, os, json
from decimal import *

import TravelDealDB as tddb
import TwitterHelper
from Airports import *

def get_airports(event, context):
    return {
       "statusCode": 200,
       "body": json.dumps(list(airport_dict.values()))
    }

def get_twitter_list_members(event, context):
    return {
        "statusCode": 200,
        "body": json.dumps(TwitterHelper.get_list_members())
    }

def convert_tweet_id(tweet):
    tweet['tweet_id'] = str(tweet['tweet_id'])
    return tweet

def get_airport_tweets(event, context):
    body = json.loads(event['body'])

    if 'airport' in body:
        response = tddb.get_tweets_by_search_criteria(body['airport'])
    else:
        response = tddb.get_any_tweet()
    
    output = list(map(convert_tweet_id, response))

    return {
        "statusCode": 200,
        "body": json.dumps(output)
    }         