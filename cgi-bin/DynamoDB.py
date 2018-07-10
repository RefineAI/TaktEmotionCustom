import boto3
import json
import yaml

import json

import decimal
#from boto3.dynamodb.conditions import Key, Attr
from collections import namedtuple



#dynamodb = boto3.resource('dynamodb')

'''
def readTable():
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('feeel-reporting-rafi')
    response = table.get_item(
        Key={
            'userId': 'antho@marin.com',
            'videoId': '2'
        }
    )
    item = response['Item']


def createTable():
    table = dynamodb.create_table(
        TableName='feeel-reporting-rafi',
        KeySchema=[
            {
                'AttributeName': 'userId',
                'KeyType': 'HASH'  #Partition key
            },
            {
                'AttributeName': 'videoId',
                'KeyType': 'RANGE'  #Sort key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'userId',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'videoId',
                'AttributeType': 'S'
            },

        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )
    print("Table status:", table.table_status)

def insertTable(jsonData):
    #print "Got Insert String: " + jsonData
    objJson = None
    table = dynamodb.Table('feeel-reporting')
    try:
        objJson = yaml.load(jsonData)
        #payload = json.loads(jsonData)
    except Exception:
        print (Exception)
    userId = str(objJson['userId'])
    videoId = str(objJson['videoId'])
    report = str(objJson['report'])

    #print "Adding row"


    table.put_item(
        Item={
            'userId':userId,
            'videoId':videoId,
            'report':report
        }
    )
    #print "Inserted Item "

def json_loads_byteified(json_text):
    return _byteify(
        json.loads(json_text, object_hook=_byteify),
        ignore_dicts=True
    )

def _byteify(data, ignore_dicts = False):
    # if this is a unicode string, return its string representation
    if isinstance(data, unicode):
        return data.encode('utf-8')
    # if this is a list of values, return list of byteified values
    if isinstance(data, list):
        return [ _byteify(item, ignore_dicts=True) for item in data ]
    # if this is a dictionary, return dictionary of byteified keys and values
    # but only if we haven't already byteified it
    if isinstance(data, dict) and not ignore_dicts:
        return {
            _byteify(key, ignore_dicts=True): _byteify(value, ignore_dicts=True)
            for key, value in data.iteritems()
        }
    # if it's anything else, return it in its original form
    return data
'''
if __name__=="__main__":
    print ("Loading DynamoDB Module")
    #readTable()
    #setupNetworks()
    #predictMetrics()