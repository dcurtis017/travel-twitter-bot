import boto3, os

topic_arn = os.environ['TWITTER_NOTIFICATION_SNS_ARN']
sns = boto3.client('sns')

def send_notification(username, number_of_new_tweets):
    sns.publish(
        TopicArn=topic_arn,
        Subject="New Flight Deals Alert",
        Message="%s there are %d new deals for your search terms"%(username, number_of_new_tweets)
    )
