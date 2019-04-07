import boto3

dynamodb = boto3.resource('dynamodb')
#dynamodb = boto3.resource('dynamodb', region_name='us-west-2', endpoint_url="http://localhost:8000")
twitter_flight_user_table = dynamodb.Table('twitter-flight-user')
twitter_flight_tweets_table = dynamodb.Table('twitter-flight-tweets')

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

# get tweets