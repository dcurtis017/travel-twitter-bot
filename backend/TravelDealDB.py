import boto3, os
from boto3.dynamodb.conditions import Key
from datetime import datetime, timedelta
from Airports import airport_cities

dynamodb = boto3.resource('dynamodb')
#dynamodb = boto3.resource('dynamodb', region_name='us-west-2', endpoint_url="http://localhost:8000")
twitter_flight_user_table = dynamodb.Table(os.environ['userTableName'])
twitter_flight_tweets_table = dynamodb.Table(os.environ['tweetsTableName'])
twitter_flight_tweets_table_created_date_index = os.environ['tweetsTableCreatedDateIndex']

# look into batch insert
def insert_tweets(tweets):
    with twitter_flight_tweets_table.batch_writer() as batch:
        for tweet in tweets:
            batch.put_item(Item=tweet)

def insert_user(user):
    return twitter_flight_user_table.put_item(Item=user)

def update_user(user):
    response = twitter_flight_user_table.update_item(
        Key = {'twitter_username': user['twitter_username']},
        UpdateExpression="set last_tweet_id=:t",
        ExpressionAttributeValues={
            ':t': user['last_tweet_id']
        },
        ReturnValues="ALL_NEW" # return all attributes
    )
    #todo : handle errors, do a conditional expression to only update the one we care about currently if the id doesn't exist, it'll add a record
    return response

def get_user_last_tweet_id(twitter_username):
    response = twitter_flight_user_table.get_item(
            Key = {'twitter_username': twitter_username}
    )
    if 'Item' in response:
        return response['Item']['last_tweet_id']
    else:
        return None

def get_tweets_by_airport_city(airport_city, limit=100):
    tweets = twitter_flight_tweets_table.query(
        KeyConditionExpression=Key('airport_city').eq(airport_city),
        ScanIndexForward=False,
        Limit=limit
    )
    if 'Items' in tweets:
        return tweets['Items']
    else:
        return []

def get_any_tweet():
    all_tweets = []
    for airport_city in airport_cities:
        tweets = get_tweets_by_airport_city(airport_city, 5)
        all_tweets+=tweets
    return all_tweets

def delete_tweets_older_than(older_than):
    # looks like delete with conditional is not supported so we have to fetch the items then batch them
    dt = datetime.now().replace(hour=0, minute=0,microsecond=0,second=0) - timedelta(days=older_than)
    dt_iso = dt.isoformat()
    for city in airport_cities:
        tweets = twitter_flight_tweets_table.query(
            IndexName = twitter_flight_tweets_table_created_date_index,
            ExpressionAttributeValues={
                ':v2':dt_iso,
                ':v1':city
            },
            KeyConditionExpression='airport_city = :v1 and created_at < :v2'
        )
        print("Will attempt to delete %d tweets for %s"%(tweets['Count'], city))
        with twitter_flight_tweets_table.batch_writer() as batch:
            for tweet in tweets['Items']:
                batch.delete_item(
                    Key={
                        'airport_city':tweet['airport_city'],
                        'tweet_id':tweet['tweet_id']
                    }
                )