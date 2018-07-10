import cognitive_face as CF
from MsTaktUtil import objToStr
import json
import operator
import numpy as np
import operator

#Key = "dcc841a853e948acb93d131f00afcb34"
Key = "15d101488ccd49f0aa7735ca0a022a8a"
CF.Key.set(Key)

emotions = ["Anger", "Contempt", "Disgust", "Fear", "Happiness", "Neutral", "Sadness", "Surprise"]

def getResponse(img_url):
    data = {}
    key = "123"
    companyId = "testCompany"
    videoId = "videoTest"
    userId = "userId"
    resp = None
    try:
        print "In MS: " + "Looking for " + img_url
        result = CF.face.detect(img_url, False, True, 'age,gender,emotion,headPose' )
        resp = json.loads(json.dumps(result))
        #
        print resp
    except Exception:
        print "Error invoking Microsoft Service" + str(Exception)
    if resp:
        data["Anger"] = resp[0]["faceAttributes"]["emotion"]["anger"]
        data["Contempt"] = resp[0]["faceAttributes"]["emotion"]["contempt"]
        data["Disgust"] = resp[0]["faceAttributes"]["emotion"]["disgust"]
        data["Fear"] = resp[0]["faceAttributes"]["emotion"]["fear"]
        data["Happiness"] = resp[0]["faceAttributes"]["emotion"]["happiness"]
        data["Neutral"] = resp[0]["faceAttributes"]["emotion"]["neutral"]
        data["Sadness"] = resp[0]["faceAttributes"]["emotion"]["sadness"]
        data["Surprise"] = resp[0]["faceAttributes"]["emotion"]["surprise"]
        data["strongestEmotion"] =  max(data.iteritems(), key=operator.itemgetter(1))[0]
        arr_list = getEmotionArray(data)
        data["class"] = max(arr_list)
        data["gender"] = resp[0]["faceAttributes"]["gender"]
        data["age"] = resp[0]["faceAttributes"]["age"]

        data["right-pupil-x"] = resp[0]["faceLandmarks"]["pupilRight"]["x"]
        data["right-pupil-y"] = resp[0]["faceLandmarks"]["pupilRight"]["y"]
        data["left-pupil-x"] = resp[0]["faceLandmarks"]["pupilLeft"]["x"]
        data["left-pupil-y"] = resp[0]["faceLandmarks"]["pupilLeft"]["y"]
        data["yaw"] = resp[0]["faceAttributes"]["headPose"]["yaw"]
        data["roll"] = resp[0]["faceAttributes"]["headPose"]["roll"]
        data["pitch"] = resp[0]["faceAttributes"]["headPose"]["pitch"]

        #print "Data is: " + str(data)
        return data


def getEmotionArray(data):
    listing = []
    listing.append(data["Anger"])
    listing.append(data["Contempt"])
    listing.append(data["Disgust"])
    listing.append(data["Fear"])
    listing.append(data["Happiness"])
    listing.append(data["Neutral"])
    listing.append(data["Sadness"] )
    listing.append(data["Surprise"] )

    return listing
