import cv2
import imutils
# import the necessary packages
from keras.preprocessing.image import img_to_array
#from keras.models import load_model
import numpy as np
import argparse

EMOTIONS = ["Anger", "Fear", "Happiness", "Sadness", "Surprise", "Neutral"]


def getROI(detector, frame):
    # resize the frame and convert it to grayscale
    frame = imutils.resize(frame, width=300)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # detect faces in the input frame
    rects = detector.detectMultiScale(gray, scaleFactor=1.1,
                                      minNeighbors=5, minSize=(30, 30),
                                      flags=cv2.CASCADE_SCALE_IMAGE)

    # ensure at least one face was found before continuing
    if len(rects) > 0:
        # determine the largest face area
        rect = sorted(rects, reverse=True,
                      key=lambda x: (x[2] - x[0]) * (x[3] - x[1]))[0]
        (fX, fY, fW, fH) = rect

        # extract the face ROI from the image, then pre-process
        # it for the network
        roi = gray[fY:fY + fH, fX:fX + fW]
        roi = cv2.resize(roi, (48, 48))
        roi = roi.astype("float") / 255.0
        roi = img_to_array(roi)
        roi = np.expand_dims(roi, axis=0)
        return roi



def detectEmotion(model, roi):
        # make a prediction on the ROI, then lookup the class
        # label
        #print ("In Keras Emo Recognition")
        result = {}
        preds = model.predict(roi)[0]
        label = EMOTIONS[preds.argmax()]
        result["class"] = preds.argmax()

        #npr = np.array(preds)
        #npr = npr.astype('str')


        result["output_prob"] = preds
        # loop over the labels + probabilities and draw them
        #for (i, (emotion, prob)) in enumerate(zip(EMOTIONS, preds)):
        #    print("***********")
        #    print(emotion)
        #    print(preds[i])
        #    result[emotion] = preds[i]
        return result
