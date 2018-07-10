#!/home/icarus/anaconda2/bin/python
from flask import Flask
from flask import g
from flask_cors import CORS, cross_origin
from flask import request, Response, stream_with_context, render_template, redirect, url_for, send_file
import cv2
from keras.models import load_model
from AWSFetchData import getImages
from Driver import get_emotion, get_emotion_image, saveToDB
from camera import VideoCamera
from MSCognitiveService import getResponse
from subprocess import call


from TaktUtils import read64
from PIL import Image

from OfflineVideoPlayback import  AnalyzeAndSaveVideo
from emotion_detector import detectEmotion, getROI

# Make sure that caffe is on the python path:
caffe_root = '/home/icarus/installs/caffe/'
import sys
from ModelUtils import getModels
sys.path.insert(0, caffe_root + 'python')

import time

import caffe
import os
import yaml
import random
import json

app = Flask(__name__, template_folder='.', static_url_path = "", static_folder = "static")

nets = {}
ageGenderCache = {}
UPLOAD_FOLDER = "/home/icarus/projects/AgeGender/cgi-bin/static/"
HTTP_PATH = "http://34.207.96.9:9000/"

def init():
    global nets
    nets = getModels()
    print "Init called"


@app.route('/aggregate', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin
def aggregate():
    print "In Aggregate"
    participantId = request.args.get("participantId")
    ageGenderCache

@app.route('/frame' ,methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def processFrame():
    print "In Frame"
    global ageGenderCache
    global nets
    data = {}
    content = request.get_json(force=True)
    #print content
    companyId = content["companyId"]
    #print companyId
    participantId = content["participantId"]
    #print participantId
    campaignId = content["campaignId"]
    #print campaignId
    image = content["image"]
    timestamp = 0
    if "timestamp" in content:
        timestamp = content["timestamp"]
    if(companyId is None or campaignId is None or participantId is None or image is None):
        return "No POST data found or missing parameters"
    start = image.find(",")
    image64 = image[start + 1:]
    data[time.time()] = image64
    print "Getting Emos"
    res = get_emotion(nets, data, companyId, campaignId, participantId, timestamp, ageGenderCache)
    #res = detectEmotion(nets["faceCascade"], nets["keras_emo"], image)
    print "Got emos"
    print res
    #res = get_emotion(nets,data, companyId, campaignId, participantId, timestamp, ageGenderCache )
    #print res
    #saveToDB(res)
    print "Sending response"
    resp = Response(response=res,
                    status=200,
                    mimetype="application/json")

    return resp

@app.route('/file',methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def uploadFile():
    display = 'Form'
    name  = None
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            print ('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            print ('No selected file')
            return redirect(request.url)
        else:
            print "Got file: " + file.filename
            prefix = random.randrange(1000, 9999)
            name = str(prefix) + "_" + file.filename
            path = UPLOAD_FOLDER + name
            file.save(os.path.join(UPLOAD_FOLDER, name))
            print("Reading file " + path)
            image = cv2.imread(path)
            print(image.shape)
            roi = getROI(nets["faceCascade"], image)
            #result = get_emotion_image(nets, path, "testCompany", "testCampaign", name, "12345", ageGenderCache)
            result = detectEmotion(nets["keras_emo"], roi)
            if(result is None):
                return "Error encountered. Please check log files"
    return '''
        <!doctype html>
        <title>Upload new File</title>
        <h1>Upload new File</h1>
        <form method=post enctype=multipart/form-data>
          <p><input type=file name=file>
             <input type=submit value=Upload>
        </form>
        <img src="''' + str(name) + '''"/>'''

@app.route('/playback')
@cross_origin()
def playback():
    print "In playback function"
    AnalyzeAndSaveVideo(nets,None)
    return render_template('index.html')


@app.route("/downloadUrl" ,methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def download():
    url = request.args.get("url")
    print "Generating random Int"
    videoId = random.randrange(1000,9999)
    print "generated random int" + str(videoId)
    fileName = "/home/icarus/projects/AgeGender/videos/" + str(videoId) + ".mp4"
    print "Dest File: " + fileName
    command = "youtube-dl -f 18 -o " + fileName +  "  " + url + " -c"
    print "Command to run: " + command
    call(command.split(), shell=False)
    #AnalyzeAndSaveVideo(nets, fileName)
    return "http://34.207.96.9:8000/stream?videoId=" + str(videoId) + ".mp4"


@app.route("/proxyStream" ,methods=['GET', 'POST' , 'OPTIONS'])
@cross_origin()
def proxyRequest():
    r = request.args.get("url", stream=True)
    return Response(r.iter_content(chunk_size=10 * 1024),
                    content_type=r.headers['Content-Type'])


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/streamWithAnnotation' ,methods=['GET', 'POST' ,'OPTIONS'])
@cross_origin()
def video_feed():
    videoId = request.args.get("videoId")
    fileName = "/home/icarus/projects/AgeGender/videos/" + "8427.mp4" #str(videoId)
    return Response(gen(VideoCamera(fileName)),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route("/stream" ,methods=['GET', 'POST' ,'OPTIONS'])
@cross_origin()
def stream():
    videoId = request.args.get("videoId")
    fileName = "/home/icarus/projects/AgeGender/videos/" + str(videoId)
    print "File to fetch: " + fileName
    g = file(fileName)  # or any generator
    return Response(g, direct_passthrough=True)


@app.route("/test" ,methods=['GET', 'POST' ,'OPTIONS'])
@cross_origin()
def processTest():
    companyId = request.args.get("companyId")
    participantId = request.args.get("participantId")
    campaignId = request.args.get("campaignId")
    return "Test processing: " + companyId + " " + participantId + " " + campaignId


@app.route("/s3" ,methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def processs3():
    companyId = request.args.get("companyId")
    participantId = request.args.get("participantId")
    campaignId = request.args.get("campaignId")
    data = getImages(companyId, campaignId, participantId)
    if(companyId is None or participantId is None or campaignId is None):
        return "Invocation is http://hostname:8000?s3?companyId=demo&campaignId=HJ8rdPEjl&participantId=water@melon.com"
    else:
        data['participantId'] = participantId
        data['companyId'] = companyId
        data['campaignId'] = campaignId
        response = get_emotion(nets, data, companyId, participantId, campaignId)
        return response


@app.route('/')
@app.route('/index')
@cross_origin()
def default():
    return "Hello There!!!"


if __name__ == '__main__':
   init()
   app.run(host='0.0.0.0', port=9000, threaded=True, debug=True)
