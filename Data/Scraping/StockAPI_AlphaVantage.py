#Final
import boto3
import pandas as pd
import io
import csv
import time
import boto3
import json
import config as cfg
from io import StringIO
from alpha_vantage.timeseries import TimeSeries

ts_json = TimeSeries(key = cfg.stock['api'])
ts_csv = TimeSeries(key = cfg.stock['api'], output_format = 'pandas')
ACCESS_KEY = cfg.aws[0]['access_key']
SECRET_KEY = cfg.aws[0]['secret_key']
BUCKET = cfg.aws[0]['bucket_name']
csv_buffer = StringIO()
s3 = boto3.client('s3', aws_access_key_id = ACCESS_KEY,
                      aws_secret_access_key = SECRET_KEY)
s3_resource = boto3.resource('s3', aws_access_key_id = ACCESS_KEY,
                      aws_secret_access_key = SECRET_KEY)
obj = s3.get_object(Bucket = BUCKET, Key = 'input.csv')
df = pd.read_csv(io.BytesIO(obj['Body'].read()))

for i,j in df.iterrows():
    data, meta_data = ts_json.get_daily(symbol = j['Ticker'], outputsize = 'full')
    df, metadata = ts_csv.get_daily(symbol = j['Ticker'], outputsize = 'full')
    meta_data["5. Category ID"] = j['Category_ID']
    meta_data["6. Category"] = j['Category']
    meta_data["7. Company ID"] = j['Company_ID']
    meta_data["8. Company Name"] = j['Company']
    meta_data["9. Market Sector"] = j['Market']
    df = df.loc['2018-03-01':'2020-03-31']
    df = df.rename(
        columns={'1. open': 'open', '2. high': 'high', '3. low': 'low', '4. close': 'close', '5. volume': 'volume'})
    df.to_csv(csv_buffer)
    s3.put_object(Body = json.dumps(data), Bucket = BUCKET,
                  Key = 'StockAPI/' + j['Category'].replace(" ","") + '/' + j['Company'].replace(" ","") + '/' + j[
                      'Company'].lower().replace(" ", "") + '.json')
    s3.put_object(Body = json.dumps(meta_data), Bucket = BUCKET,
                  Key = 'StockAPI/' + j['Category'].replace(" ","") + '/' + j['Company'].replace(" ","") + '/' + j[
                      'Company'].lower().replace(" ", "") + '_metadata.json')
    s3_resource.Object(bucket_name = BUCKET, key = 'StockAPI/' + j['Category'].replace(" ","") + '/' + j['Company'].replace(" ","") + '/' +
                   j['Company'].lower().replace(" ", "") + '.csv').put(Body = csv_buffer.getvalue())