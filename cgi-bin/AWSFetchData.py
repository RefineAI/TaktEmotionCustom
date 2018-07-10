#!/home/icarus/anaconda2/bin/python
import boto3
import os
import yaml
BASE_DIRECTORY="/home/icarus/projects/real-time_emotion_analyzer/downloads/"

def makeDirs(companyId, campaignId, participantId):
    destinationPath = BASE_DIRECTORY + companyId + "/" + campaignId + "/"
    #print "DestPath: " + destinationPath
    try:
        os.makedirs(destinationPath)
    except:
        if not os.path.isdir(destinationPath):
            raise
    destinationFilePath = destinationPath + participantId + ".txt"
    with open(destinationFilePath, 'w') as f:
        print
        #print "File created: " +  destinationFilePath

def getDataFromS3(companyId, campaignId, participantId):
    localFile = BASE_DIRECTORY + companyId + "/" + campaignId + "/" + participantId + ".txt"
    bucketKey = companyId + "/" + campaignId + "/" + participantId
    #print "bucket key: " + bucketKey
    makeDirs(companyId, campaignId, participantId)
    #s3 = boto3.resource('s3')
    #bucket = s3.Bucket('emotely-frames')
    s3 = boto3.client('s3')
    s3.download_file('emotely-frames', bucketKey, localFile)
    print ("Download Complete")
    #s3.download_file(bucket, bucketKey, localFile)

def getImages(companyId, campaignId, participantId):
    data = None
    images = {}
    getDataFromS3(companyId,campaignId, participantId)
    localFile = BASE_DIRECTORY + companyId + "/" + campaignId + "/" + participantId + ".txt"
    with open(localFile, 'r') as json:
        data = json.read()
    json = yaml.load(data)
    #print json['participantId']
    for image in json["imageArray"]:
        timestamp = image['timestamp']
        #print  timestamp
        image64 =   image['image']
        start = imageCleaned = image64.find(",")
        image64 = image64[start+1: ]
        #print image64
        images[timestamp] = image64
    os.remove(localFile)
    return images

if "__name__"  == "__main__":
    getDataFromS3("demo", "HJ8rdPEjl", "water@melon.com")