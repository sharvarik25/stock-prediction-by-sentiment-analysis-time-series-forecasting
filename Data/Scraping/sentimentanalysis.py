import boto3
import pandas as pd
import io
import csv
import time
import boto3
import json
import config as cfg
from io import StringIO
csv_buffer = StringIO()


ACCESS_KEY = cfg.aws[0]['access_key']
SECRET_KEY = cfg.aws[0]['secret_key']
BUCKET = cfg.aws[0]['bucket_name']
s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY,
                      aws_secret_access_key=SECRET_KEY)
s3_resource = boto3.resource('s3', aws_access_key_id = ACCESS_KEY, aws_secret_access_key = SECRET_KEY)
obj = s3.get_object(Bucket= BUCKET, Key= 'Final_content/Year/*.csv')
for item in obj:
    df = pd.read_csv(io.BytesIO(obj['Body'].read()))
    sentiment = []
    positive = []
    negative = []
    neutral = []
    mixed = []
    for row in df['headline']:
        print(row)
        response = comprehend.detect_sentiment(Text=row, LanguageCode="en")
        sentiment.append(response['Sentiment'])
        positive.append(response['SentimentScore']['Positive'])
        negative.append(response['SentimentScore']['Negative'])
        neutral.append(response['SentimentScore']['Neutral'])
        mixed.append(response['SentimentScore']['Mixed'])
        df['Sentiment'] = sentiment
        df['Positive Score'] = positive
        df['Negative Score'] = negative
        df['Neutral Score'] = neutral
        df['Mixed Score'] = mixed
        df.to_csv(csv_buffer)
        s3_resource.Object(BUCKET, 'SentimentScore/' + item + '.csv').put(Body=csv_buffer.getvalue())


