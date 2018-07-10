import cv2
import base64
import skvideo.io

from skvideo.io import VideoWriter
import sys

videoFile = "/home/icarus/projects/AgeGender/videos/9980.mp4"

faceCascade = "/home/icarus/projects/AgeGender/cgi-bin/haarcascade_frontalface_default.xml"
cascade = cv2.CascadeClassifier(faceCascade)

try:
    cap = skvideo.io.VideoCapture(videoFile)
except:
    print "problem opening input stream " + videoFile
    sys.exit(1)
if not cap.isOpened():
    print "capture stream not open " + videoFile
    sys.exit(1)