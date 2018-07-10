import numpy as np
import os
import sys

import FileVideoStream
import fps

import skvideo.io

#from skvideo.io import VideoWriter
import numpy

#Install using pip install scikit-video

import time

'''
   Opencv Stuff
'''
caffe_root="/home/icarus/installs/caffe/"
sys.path.insert(0, caffe_root + 'python')

import cv2
import caffe

caffe.set_mode_gpu()
caffe.set_device(0)


DEMO_DIR = "/home/icarus/projects/AgeGender/model/DemoDir/"
MODEL_DIR = "/home/icarus/projects/AgeGender/model/"
categories = [ 'Angry', 'Disgust', 'Fear', 'Happy', 'Neutral',  'Sad', 'Surprise']
gender_list = ['Male', 'Female']
age_list=['(0, 2)','(4, 6)','(8, 12)','(15, 20)','(25, 32)','(38, 43)','(48, 53)','(60, 100)']

#nets = []

#video_capture = cv2.VideoCapture(0)


def setupNet():
    nets = {}
    mean_filename = os.path.join(DEMO_DIR, "VGG_S_rgb", 'mean.binaryproto')


    net_pretrained = os.path.join(DEMO_DIR, "VGG_S_rgb", 'EmotiW_VGG_S.caffemodel')
    net_model_file = os.path.join(DEMO_DIR, "VGG_S_rgb", 'deploy.prototxt')
    VGG_S_Net = caffe.Classifier(net_model_file, net_pretrained,
                                 # mean=mean,
                                 channel_swap=(2, 1, 0),
                                 raw_scale=255,
                                 image_dims=(256, 256))
    nets["emotion"] =VGG_S_Net

    AGE_MODEL_FILE = '/home/icarus/projects/AgeGender/model/deploy_age.prototxt'
    AGE_PRETRAINED = '/home/icarus/projects/AgeGender/model/age_net.caffemodel'

    GENDER_MODEL_FILE = '/home/icarus/projects/AgeGender/model/deploy_gender.prototxt'
    GENDER_PRETRAINED = '/home/icarus/projects/AgeGender/model/gender_net.caffemodel'



    age_net = caffe.Classifier(AGE_MODEL_FILE, AGE_PRETRAINED,
                               # mean = mean,
                               # mean=np.load(caffe_root + 'python/caffe/imagenet/ilsvrc_2012_mean.npy').mean(1).mean(1),
                               channel_swap=(2, 1, 0),
                               raw_scale=255,
                               image_dims=(256, 256))
    # input_image = caffe.io.load_image(IMAGE_FILE)

    nets["age"] = age_net

    gender_net = caffe.Classifier(GENDER_MODEL_FILE, GENDER_PRETRAINED,
                                  # mean = mean,
                                  # mean=np.load(caffe_root + 'python/caffe/imagenet/ilsvrc_2012_mean.npy').mean(1).mean(1),
                                  channel_swap=(2, 1, 0),
                                  raw_scale=255,
                                  image_dims=(256, 256))
    # input_image = caffe.io.load_image(IMAGE_FILE)


    nets["gender"] = gender_net

    return nets



def AnalyzeAndSaveVideo(net, videoFile):
    # Define the codec and create VideoWriter object
    (major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')
    #print major_ver
    #print minor_ver
    if net is None:
        net = setupNet()

    #writer = VideoWriter("/home/icarus/projects/AgeGender/videos/output.mp4", frameSize=(360, 640))
    #writer.open()
    #Didn'r do this image = numpy.zeros((h, w, 3))
    if videoFile is None:
        videoFile = "/home/icarus/projects/AgeGender/videos/6323.mp4"

    fourcc = cv2.VideoWriter_fourcc(*'AVCI')
    out = cv2.VideoWriter('/home/icarus/projects/AgeGender/videos/output.mp4', fourcc, 1.0, (640, 480))
    faceCascade = "/home/icarus/projects/AgeGender/cgi-bin/haarcascade_frontalface_default.xml"
    HOW_MANY_FRAMES_TO_SKIP_FROM_CURRENT_FRAME = 20

    #videoFile = "/home/icarus/projects/AgeGender/videos/FB7LoFgv5cA.mp4"

    cascade = cv2.CascadeClassifier(faceCascade)

    try:
        cap = skvideo.io.VideoCapture(videoFile)
    except:
        print "problem opening input stream " + videoFile
        sys.exit(1)
    if not cap.isOpened():
        print "capture stream not open " + videoFile
        sys.exit(1)

    frameId = 0
    nextFrameId = 0 + 10
    startTime = time.time()
    while(cap.isOpened()):
        ret, frame = cap.read()
        frameId = frameId + 1

        if (frameId < nextFrameId):
            continue

        nextFrameId = frameId + HOW_MANY_FRAMES_TO_SKIP_FROM_CURRENT_FRAME
        if(frame is None):
            #print "Frame is of type None. Breaking  loop"
            continue
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE
        )
        if (len(faces) > 0):
            print "\t\t\t\t Faces : " + str(len(faces))
        for i, f in enumerate(faces):
            x, y, w, h = [v for v in f]
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 255))
            frame = frame / 255.
            input_image = frame[:, :, (2, 1, 0)]
            sub_face = input_image[y:y + h, x:x + w]
            s = time.time()
            emotion = net["emotion"].predict([sub_face], oversample=False)
            e = time.time()
            print "Emotion: " + str(e-s)
            s = time.time()
            age = net["age"].predict([sub_face])
            e = time.time()
            print "Age: " + str(e-s)
            s = time.time()
            gender = net["gender"].predict([sub_face])
            e=time.time()
            print "Gender: " + str(e-s)
            s = time.time()
            emotion = categories[emotion.argmax()]
            age = age_list[age[0].argmax()]
            gender = gender_list[gender[0].argmax()]
            text = emotion + " : " + age + " : " + gender
            e = time.time()
            print "\t\t\t\t Face: " + str(i) + " has: " + text +  " " + "Frame: " +  str(frameId)
            font = cv2.FONT_HERSHEY_SIMPLEX
            x = x + w  # position of text
            y = y + w  # position of text
            cv2.putText(frame, text, (x, y), font, 6, (200, 255, 155), 13, cv2.LINE_AA)
            s = time.time()
            out.write(frame)
            e = time.time()
            print "Write to file: " + str(e-s)
            print "\t\t\t\t Face pisitons: X " + str(x) + "  Y: " + str(y)
    print "Done processing. Releasing Video Stream!!"
    cap.release()
    #writer.release()
    #cv2.destroyAllWindows()

'''
    End Opencv
'''

#cAnalyzeAndSaveVideo(None, None)



