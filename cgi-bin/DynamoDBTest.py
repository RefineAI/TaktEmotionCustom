from DynamoDB import createTable
from DynamoDB import insertTable
import boto3
import json
import re

import yaml

def TestCreateTable():
    print "Creating Table"
    createTable()
    print "Created Table"

def TestInsertTable():
    print "Inserting row"
    jString = getString()
    objJson = yaml.load(jString)
    print objJson['userId']
    insertTable(jString)
    print "Inserted row"


def getString():
    data = '''{
    'userId': 123,
    'videoId' : 'test',
     'report': [
        'customer':{
            'clientId': 'antho@marin.com','companyId': 'takt', 'campaignId': '2','timestamp': '0'
        },
         'eyes':{
        },
        'head':{
        },
        'appearance': {
            'age': '(38, 43)', 'ethnicity': 'Caucasian', 'gender':'Male', 'glasses': 'glasses'
        },
        'emotions': {
        'anger': '0.026568742469','fear': '0.0036776275374','joy': '0.00349514069967','sad': '0.0489134378731', 'surprise': '5.05143871123e-05', 'neutral': '4.33194691141e-05', 'disgust': '0.89475518465', 'contempt': '0.0224959440529', 'engagement': '0.829962656119', 'valence': '0.664427533358'
        },
        'emotion': {
        'emotion':'Disgust'
        }
    ]}
    '''

    return data


if __name__=="__main__":
    print "Loading DynamoDB Module"
    #TestCreateTable()
    #TestInsertTable()
    #predictMetrics()










