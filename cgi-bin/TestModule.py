#!/home/icarus/anaconda2/bin/python
import cv2
import os
import skvideo.io
from TaktUtils import *
import base64
from ModelUtils import *

from Driver import *

from MSCognitiveService import getResponse


TEST_VIDEO_FILE ="/home/icarus/projects/AgeGender/videos/9980.mp4"
TEST_IMAGE_FOLDER = "/home/icarus/projects/AgeGender/images"

UPLOAD_FOLDER = "/home/icarus/projects/AgeGender-Dev/cgi-bin/static/"
HTTP_PATH = "http://34.207.96.9:9000/"

nets = {}
ageGenderCache = {}

def init():
    global nets
    nets = getModels()

def testImage(path):
    print "Testing Image"
    res = getResponse("/home/icarus/projects/AgeGender-Dev/images/OldMan.jpeg")
    print res


def testVideo():
    print "Testing Video"
    data = {}
    videoFile = "/home/icarus/projects/AgeGender-Dev/videos/4058.mp4"
    #cap = skvideo.io.VideoCapture(videoFile)
    print "Before Cap"
    cap = cv2.VideoCapture(videoFile)
    print "After Cap"
    participantId = "abcde"
    i = 0
    while (cap.isOpened()):
        print "cap opened successfully"
        ret, frame = cap.read()
        if(ret):
            if (i % 200 == 0):
                try:
                    cnt = cv2.imencode('.jpg', frame)[1]
                    base64Str = base64.b64encode(cnt)
                    data[time.time()] = base64Str

                    frame = read64(base64Str)

                    img_name = str(participantId) + ".jpeg"

                    path = UPLOAD_FOLDER + str(participantId) + ".jpeg"
                    cv2.imwrite(path, frame)
                    image_url = HTTP_PATH + img_name
                    print str("############") + " Image URL: " + image_url


                    # emo = get_emotion(nets, data, "companyTest", "123456", "Video123", time.time(), ageGenderCache)
                    print str("**************************")
                    #print res
                    print str("**************************")
                    print "Iteration: " + str(i)
                except:
                    print "Exception in OpenCV. Moving on"
                    pass
        else:
            print "Fialed to get Frame : " + str(i)

        i = i + 1



if __name__=="__main__":
    print "In testing module"
    init()
    #testVideo()
    testImage("blah")
