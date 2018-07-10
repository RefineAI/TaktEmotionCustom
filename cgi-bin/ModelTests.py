import os
import time
import numpy as np
import cv2
import caffe
import sys
import skvideo.io
from skvideo.io import VideoWriter
from  AgeGenderDetector import setupNetworks
from AgeGenderDetector import predictMetrics

caffe.set_mode_gpu()
caffe.set_device(0)

caffe_root="/home/icarus/installs/caffe/"
DEMO_DIR = "/home/icarus/projects/AgeGender/model/DemoDir/"
IMAGE_DIR = "/home/icarus/projects/AgeGender/images/"
sys.path.insert(0, caffe_root + 'python')
categories = [ 'Angry', 'Disgust', 'Fear', 'Happy', 'Neutral',  'Sad', 'Surprise']
dir_names = ["VGG_S_rgb", "VGG_S_lbp", "VGG_S_cyclic_lbp", "VGG_S_cyclic_lbp_5","VGG_S_cyclic_lbp_10"]

emoNet = {}

def initNets():
    global emoNet
    emoNet = setupNetworks()
    #for cur_net_dir in dir_names:
    #    print dir
        #mean_filename = os.path.join(DEMO_DIR, cur_net_dir, 'mean.binaryproto')
        #proto_data = open(mean_filename, "rb").read()
        #a = caffe.io.caffe_pb2.BlobProto.FromString(proto_data)
        #mean = caffe.io.blobproto_to_array(a)[0]

    #    net_pretrained = os.path.join(DEMO_DIR, cur_net_dir, 'EmotiW_VGG_S.caffemodel')
    #   net_model_file = os.path.join(DEMO_DIR, cur_net_dir, 'deploy.prototxt')
    #   VGG_S_Net = caffe.Classifier(net_model_file, net_pretrained,
    #                                 # mean=mean,
    #                                 channel_swap=(2, 1, 0),
    #                                 raw_scale=255,
    #                                 image_dims=(256, 256))
    #    nets.append(VGG_S_Net)

    print "Done initializing Nets. Prediction begins!!"

def DetectFace(image):
    metric = {}

    faceCascade = "/home/icarus/projects/AgeGender/cgi-bin/haarcascade_frontalface_default.xml"
    facedata = "haarcascade_frontalface_default.xml"
    cascade = cv2.CascadeClassifier(facedata)
    if type(image) is str:
        img = cv2.imread(image)
    else:
        img = image
    minisize = (img.shape[1], img.shape[0])
    miniframe = cv2.resize(img, minisize)
    faces = cascade.detectMultiScale(
        miniframe,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )
    global sub_face
    sub_face = None

    for f in faces:
        x, y, w, h = [v for v in f]
        sub_face = img[y:y + h, x:x + w]
        metric["good-to-determine-gender"] = img
        metric["good-to-determine-age"] = sub_face
        metric["good-to-determine-emotion"] = sub_face
        metric["miniframe"] = miniframe
    #return sub_face
    return metric

def processFiles():
    initNets()
    for root, directories, filenames in os.walk(IMAGE_DIR):
        for directory in directories:
            print os.path.join(root, directory)
        for filename in filenames:
            filename = os.path.join(root, filename)

            print filename
            if filename.startswith(".") or os.path.isdir(filename):
                continue


            options = DetectFace(filename)

            if not  options:
                print "Skipping file, no face found: " + filename
                continue
            sub_face = options["good-to-determine-age"]
            img = options["good-to-determine-gender"]
            img = img / 255.
            input_image = img[:, :, (2, 1, 0)]

            sub_face = sub_face /255.
            sub_face = sub_face[:,:, (2,1,0)]

            #input_image_caffe = caffe.io.load_image(filename)


            print
            print str("******************")
            print  "\t\t\t\t" + str(predictMetrics(input_image, filename, emoNet))
            print str("*********************")
            print



def processVideo():
    initNets()
    videoFile = "/home/icarus/projects/AgeGender/videos/1418.mp4"
    cap = skvideo.io.VideoCapture(videoFile)
    while (cap.isOpened()):
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        img = DetectFace(gray)
        if img is None:
            "No Face! Skipping Frame"
            continue
        #print img.shape
        img = img / 255.
        input_image = img[:, :, (2, 1, 0)]
        print
        print  "\t\t\t\t" + str(predictMetrics(None, None, input_image, None, emoNet))
        print


if __name__=="__main__":
    #processVideo()
    processFiles()


