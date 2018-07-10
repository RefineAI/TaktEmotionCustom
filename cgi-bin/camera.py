#!/home/icarus/anaconda2/bin/python
import cv2
import skvideo.io
#from skvideo.io import VideoWriter
import time




class VideoCamera(object):
    def __init__(self, videoFile):
        print "Camera Initialized"
        # Using OpenCV to capture from device 0. If you have trouble capturing
        # from a webcam, comment the line below out and use a video file
        # instead.
        print "Video File: " + videoFile
        self.video = skvideo.io.VideoCapture(videoFile)
        #self.video = cv2.VideoCapture(videoFile)
        #self.video =  skvideo.io.VideoCapture("/home/icarus/projects/MultiThreadPython/yttest.mp4")
        # If you decide to use video.mp4, you must have this file in the folder
        # as the main.py.
        # self.video = cv2.VideoCapture('video.mp4')

    def __del__(self):
        self.video.release()


    def get_frame(self):
        success, frame = self.video.read()
        image = frame
        faceCascade = "/home/icarus/projects/AgeGender/cgi-bin/haarcascade_frontalface_default.xml"
        cascade = cv2.CascadeClassifier(faceCascade)
        # We are using Motion JPEG, but OpenCV defaults to capture raw images,
        # so we must encode it into JPEG in order to correctly display the
        # video stream.
        #print frame.shape
        img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY, 1)

        faces = cascade.detectMultiScale(
            img_gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            flags=0
        )
        #emotions = []
        # Draw a rectangle around the faces
        for (x, y, w, h) in faces:
            #face_image_gray = img_gray[y:y + h, x:x + w]
            cv2.rectangle(image, (x, y), (x + w, y + h), (84,206,238), 2)
           # values =  self.predict_emotion(face_image_gray, model)
           # maxindex = values.index(max(values))
           # emotion = emotion_labels[maxindex]
           # cv2.putText(image, emotion, (x, y - 10), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0),2)
        ret, jpeg = cv2.imencode('.jpg', image)
        print "Returning frame"
        return jpeg.tobytes()