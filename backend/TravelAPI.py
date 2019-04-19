import tweepy, os, json
from decimal import *
from json.decoder import JSONDecodeError

import TravelDealDB as tddb
import TwitterHelper
from Airports import *

def get_airports(event, context):
    return {
       "statusCode": 200,
       "body": json.dumps(airport_dict)
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
    try:
        body = json.loads(event['body'])
    except (JSONDecodeError, KeyError, TypeError) as e:
        print("%s will return latest results"%type(e).__name__)
        body = {}

    if 'airport_city' in body:
        response = tddb.get_tweets_by_airport_city(body['airport_city'])
    else:
        response = tddb.get_any_tweet()

    output = list(map(convert_tweet_id, response))

    return {
        "statusCode": 200,
        "body": json.dumps(output)
    }