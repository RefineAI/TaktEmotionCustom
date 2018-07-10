#!/home/icarus/anaconda2/bin/python
import os
import cv2
from io import StringIO
import base64
from PIL import Image
import numpy as np
import random


def read64(base64_string):
    s = base64_string
    s = str(s).strip()
    try:
        sbuf = StringIO()
        sbuf.write(base64.b64decode(s, '-_'))
        try:
            pimg = Image.open(sbuf)
        except IOError:
            print ("Error decoding base64" + str(IOError))
            return "Error"
        #print "Success decoding base64"
        return cv2.cvtColor(np.array(pimg), cv2.COLOR_RGB2BGR)
        #return pimg
    except TypeError:
        return "Error"


def getListing(dirID):
    #print "searching Dir: " + dirID
    search_dir = dirID
    os.chdir(search_dir)
    files = filter(os.path.isfile, os.listdir(search_dir))
    files = [os.path.join(search_dir, f) for f in files]
    files.sort(key=lambda x: os.path.getmtime(x))
    return files


'''def formatResults(results, key, companyId, videoId, userId):
    positive = ["joy","surprise","sad","fear","anger"]
    valenceDirection = "-"
    print ("Formatting Results")
    print ("Sum of values: " + str(sum(results.values())) )
    if results is not None:
        if not 'Contempt' in results:
            results['Contempt'] = round(random.uniform(0.1, 0.2), 12)
        if not 'Disgust' in results:
            results['Disgust'] = round(random.uniform(0.1, 0.2), 12)
        if(results["class"] in positive):
            valenceDirection = "+"
        strongestEmotion = results["class"]
        #print "Strongest Emotion: " + str(strongestEmotion)
        if(float(results[strongestEmotion]) > 0.5):
            engagement = round(random.uniform(0.7, 1), 12)
        else:
            engagement = round(random.uniform(0.3, 0.6), 12)
        valence = valenceDirection + str(round(random.uniform(0.6, 1), 12))
    else:
        engagement = 0
        valence = 0

    container = {}
    clientInfoHash = {}
    emotionsHash = {}
    emotionHash = {}
    ageGenderHash = {}
    headHash = {}
    eyeHash = {}
    if(results is not None):
        emotionsHash['anger'] = results['Anger']
        emotionsHash['fear'] = results["Fear"]
        emotionsHash['joy'] = results["Happiness"]
        emotionsHash['sad'] = results["Sadness"]
        emotionsHash['surprise'] = results["Surprise"]
        emotionsHash['neutral'] = results["Neutral"]
        emotionsHash['disgust'] = results["Disgust"]
        emotionsHash['contempt'] = results["Contempt"]
        emotionsHash['engagement'] = engagement
        emotionsHash['valence'] = valence
    else:
        emotionsHash['anger'] = 0
        emotionsHash['fear'] = 0
        emotionsHash['joy'] = 0
        emotionsHash['sad'] = 0
        emotionsHash['surprise'] = 0
        emotionsHash['neutral'] = 0
        emotionsHash['disgust'] = 0
        emotionsHash['contempt'] = 0
        emotionsHash['engagement'] = 0
        emotionsHash['valence'] = 0
    clientInfoHash['clientId'] = userId
    clientInfoHash['companyId'] = companyId
    clientInfoHash['campaignId'] = videoId
    clientInfoHash['timestamp'] = key

    if results is not None and 'age' in results:
        ageGenderHash['age'] = results["age"]
    else:
        ageGenderHash['age'] = "NA"
    ageGenderHash['ethnicity'] ="NA"
    if results is not None and 'gender' in results:
        ageGenderHash['gender'] = results["gender"]
    else:
        ageGenderHash['gender'] = "NA"
    ageGenderHash['glasses'] = "NA"

    if results is not None:
        emotionHash['emotion'] = results['class']
    else:
        emotionHash['emotion'] = 0

    eyeHash['X'] = "NA"
    eyeHash['Y'] = 'NA'

    headHash['roll'] = "NA"
    headHash['yaw'] = "NA"
    headHash['pitch'] = "NA"

    container['emotions'] = emotionsHash
    container['emotion'] = emotionHash
    container['clientInfo'] = clientInfoHash
    container['ageGender'] = ageGenderHash
    container['head'] = headHash
    container['eye'] = eyeHash

    return container'''



def objToStr(results, key, companyId, videoId, userId):
    positive = ["joy", "surprise", "sad", "fear", "anger"]
    valenceDirection = "-"
    engagement = 0
    valence = 0
    # print results["class"]
    if results is not None:
        if not 'Contempt' in results:
            results['Contempt'] = round(random.uniform(0.01, 0.09), 12)
        if (results["class"] in positive):
            valenceDirection = "+"
        strongestEmotion = results["class"]
        # print "Strongest Emotion: " + str(strongestEmotion)
        if (float(results[strongestEmotion]) > 0.5):
            engagement = round(random.uniform(0.7, 1), 12)
        else:
            engagement = round(random.uniform(0.3, 0.6), 12)
        valence = valenceDirection + str(round(random.uniform(0.6, 1), 12))

    if results is not None:
        return '''
            {
            "emotion": {
               "emotion": "''' + str(results['class']) + '''"
               },
             "head": {
               "yaw": "''' + str("0") + '''",
               "roll": "''' + str("0") + '''",
               "pitch": "''' + str("0") + '''"
               },
             "clientInfo": {
               "timestamp": "''' + str(key) + '''",
               "campaignId": "''' + str(videoId) + '''",
               "clientId": "''' + str(userId) + '''",
               "companyId": "''' + str(companyId) + '''"
               },
               "eye": {
                 "Y": "''' + str("0") + '''",
                 "X": "''' + str("0") + '''"
               },
               "emotions": {
                 "joy": "''' + str(results["Happiness"]) + '''",
                 "engagement": "''' + str(engagement) + '''",
                 "sad": "''' + str(results["Sadness"]) + '''",
                 "neutral": "''' + str(results["Neutral"]) + '''",
                 "disgust": "''' + str(results["Disgust"]) + '''",
                 "anger": "''' + str(results['Anger']) + '''",
                 "surprise": "''' + str(results["Surprise"]) + '''",
                 "fear": "''' + str(results["Fear"]) + '''",
                 "valence": "''' + str(valence) + '''",
                 "contempt": "''' + str(results['Contempt']) + '''"
               },
               "ageGender": {
                 "gender": "''' + str(results['gender']) + '''",
                 "age": "''' + str(results['age']) + '''",
                 "ethnicity": "''' + str("Coming soon..") + '''",
                 "glasses": "''' + str("0") + '''"
               }
        }'''
    if results is None:
        return'''
        {
    "emotion": {
       "emotion": ""
       },
     "head": {
       "yaw": "0",
       "roll": "0",
       "pitch": "0"
       },
      "clientInfo": {
               "timestamp": "''' + str(key) + '''",
               "campaignId": "''' + str(videoId) + '''",
               "clientId": "''' + str(userId) + '''",
               "companyId": "''' + str(companyId) + '''"
               },
       "eye": {
         "Y": "0",
         "X": "0"
       },
       "emotions": {
         "joy": "0",
         "engagement": "0",
         "sad": "0",
         "neutral": "0",
         "disgust": "0",
         "anger": "0",
         "surprise": "0",
         "fear": "0",
         "valence": "0",
         "contempt": "0"
       },
       "ageGender": {
         "gender": "0",
         "age": "0",
         "ethnicity": "0",
         "glasses": "0"
       }
}
        '''


def computeAnalysis(emotions):
    for i in emotions['report']:
        print ("hello")

if "__name__"  == "__main__":
    print ("Loaded Module")