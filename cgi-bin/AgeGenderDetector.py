#!/home/icarus/anaconda2/bin/python
import numpy as np
#import matplotlib.pyplot as plt

# Make sure that caffe is on the python path:
caffe_root = '/home/icarus/installs/caffe/'  # this file is expected to be in {caffe_root}/examples
import sys
import cv2
from EmotionDetector import setup
from EmotionDetector import class_img
sys.path.insert(0, caffe_root + 'python')
from emotion_detector import detectEmotion, getROI

import time
from MSCognitiveService import getResponse

import caffe
import os
import yaml
import operator
import json

HTTP_PATH = "http://34.207.96.9:8000/"
TEMP_FRAME_STORE = "/home/icarus/projects/AgeGender/cgi-bin/static/"

caffe.set_mode_gpu()
caffe.set_device(0)


def predictMetricsWithMicrosoft(frame, emotionFrame, nets, ageGenderCache, participantId):
    print ("In M$ Metrics")
    resp = getResponse(emotionFrame)
    return resp



def predictMetrics(frame, emotionFrame, nets, ageGenderCache, participantId):
    caffe.set_mode_gpu()
    caffe.set_device(0)
    age_list=['(0, 2)','(4, 6)','(8, 12)','(15, 20)','(25, 32)','(38, 43)','(48, 53)','(60, 100)']
    gender_list=['Male','Female']
    caffe_list = ['Neutral', 'Anger', 'Contempt', 'Disgust', 'Fear', 'Happiness', 'Sadness', 'Surprise']
    vgg_list =  [ 'Anger', 'Disgust', 'Fear', 'Happiness', 'Neutral',  'Sadness', 'Surprise']
    keras_list = ["Anger", "Fear", "Happiness", "Sadness", "Surprise", "Neutral"]
    age_net = nets['age']
    emotion_net = nets['keras_emo']
    gender_net = nets['gender']
    vgg = nets['vgg']
    age = None
    gender = None
    emotion = None

    if age_net is not None:
        s = time.time()
        prediction = age_net.predict([frame])
        age = age_list[prediction[0].argmax()]
        print ("Age: " + age)
        e = time.time()
        #print "age prediction took: " + str(e - s)

    if gender_net is not None:
        s = time.time()
        prediction = gender_net.predict([frame])
        gender = gender_list[prediction[0].argmax()]
        print ("Gender: " + gender)
        e = time.time()
        #print "gender prediction took: " + str(e -s)

    '''if participantId not in ageGenderCache:
        img_name = str(participantId) + ".jpeg"
        img_path = TEMP_FRAME_STORE + str(participantId) + ".jpeg"
        image_url = HTTP_PATH + img_name
        print (str("############" ) + " Image URL: " + image_url)
        res = class_img(image_url,nets)
        age = res["age"]
        print (age)
        gender = res["gender"]
        print (gender)
        storeInCache(ageGenderCache, participantId, age, gender)
    else:
        #print "Age Gender from Cache"
        age = ageGenderCache[participantId][0]
        gender = ageGenderCache[participantId][1]'''

    if vgg is not None:
        prediction = vgg.predict([frame])
        print (str(prediction))
        vgg_emo = vgg_list[prediction[0].argmax()]
        #print str("*****************[AgeGenderDetector.py]")
        vgg_emo_str =  json.dumps({"class": prediction[0].argmax(), "output_prob": prediction[0].tolist()})
        print ("VGG: " + vgg_emo)
        #print "VGG List: " + vgg_emo_str


    if emotion_net is not None:
        s = time.time()
        #prediction = class_img(emotionFrame, emotion_net)
        image = cv2.imread(emotionFrame)
        roi = getROI(nets["faceCascade"], image)
        #print "Calling Keras emotion detector...[AgeGenderDetector.py]"
        prediction = detectEmotion(nets["keras_emo"], roi)
        e = time.time()
        #print "emotion prediction took: " + str(e - s) + "[AgeGenderDetector.py]"
        emotion_str = json.dumps({"class": prediction["class"], "output_prob": prediction["output_prob"].tolist()})
        print ("Keras: " + keras_list[prediction["class"]])
        #print "Emotion String is: " + emotion_str + "[AgeGenderDetector.py]"


    preds = {}
    #result = yaml.load(vgg_emo_str)
    result = yaml.load(emotion_str)
    emotions = result["output_prob"]


    preds["Disgust"] = 0
    preds["Contempt"] = 0

    for index, item in enumerate(emotions):
        #preds[vgg_list[index]] = item
        preds[keras_list[index]] = item


    #preds["class"] = current_list[result["class"]]
    #preds["class"] = vgg_list[result["class"]]
    preds["class"] = keras_list[result["class"]]

    preds["age"] = age
    preds["gender"] = gender
    img_path = TEMP_FRAME_STORE + str(participantId) + ".jpeg"
    print ("Removing : " + img_path)
    os.remove(img_path)
    #print "Preds are: " + str(preds)
    return preds


def storeInCache(ageGenderCache, participantId, age, gender):
    print ("No Entry Found. Creating One for: " + str(participantId))
    ageGenderCache[participantId] = []
    ageGenderCache[participantId].append(age)
    ageGenderCache[participantId].append(gender)


'''def checkMajorityPrediction(ageGenderCache, participantId, ageKey, genderKey):
    majorityAge = ageKey
    majorityGender = genderKey
    if participantId in ageGenderCache:
            global computedAge
            global computedGender

            #print "Found Entry: " + str(ageKey) + " " + str(ageKey)

            if ageKey not in ageGenderCache[participantId][0]:
                ageGenderCache[participantId][0][ageKey] = 0
            if genderKey not in ageGenderCache[participantId][1]:
                ageGenderCache[participantId][1][genderKey] = 0

            age = ageGenderCache[participantId][0][ageKey]
            gender = ageGenderCache[participantId][1][genderKey]
            ageCount = age+1
            genderCount = gender+1

            ageGenderCache[participantId][0][ageKey] = ageCount
            ageGenderCache[participantId][1][genderKey] = genderCount

            majorityAge = max(ageGenderCache[participantId][0].iteritems(), key=operator.itemgetter(1))[0]
            majorityGender = max(ageGenderCache[participantId][1].iteritems(), key=operator.itemgetter(1))[0]

    else:
        print ("No Entry Found. Creating One")
        ageGenderCache[participantId] = [{}, {}]
        ageGenderCache[participantId][0][ageKey] = 0
        ageGenderCache[participantId][1][genderKey] = 0
    result = {}
    result["age"] = majorityAge
    result["gender"] = majorityGender
    print (str(ageGenderCache))
    return result'''

if __name__=="__main__":
    print ("Loading Module")
    #setupNetworks()
    #predictMetrics()

