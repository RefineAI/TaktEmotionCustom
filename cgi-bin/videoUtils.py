import cv2



def getFaces(gray_frame, faceCascade):
    #print "Getting Faces"
    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(
        gray_frame,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )
    return faces

def getSmiles(roi_gray, count, smileCascade):
    foundSmile = False
    sF = 1.65
    if(count > 4):
        sF = 1.05
    #print "Getting Smiles for: " + str(count) + " with sF: " + str(sF)
    smile = smileCascade.detectMultiScale(
        roi_gray,
        #scaleFactor=1.7,
        #minNeighbors=22,
        scaleFactor = sF,
        minNeighbors=22,
        minSize=(25, 25),
        flags=cv2.CASCADE_SCALE_IMAGE
    )
    for (x, y, w, h) in smile:
        #print "Found", len(smile), "smiles!"
        foundSmile = True
        #cv2.rectangle(color_frame, (x, y), (x + w, y + h), (255, 0, 0), 1)
        #font = cv2.FONT_HERSHEY_SIMPLEX
        #cv2.putText(color_frame, "Happy", (x, y + 10), font, 1, (255, 0, 0), 2)
        # print "!!!!!!!!!!!!!!!!!"
    return foundSmile


def getEyes():
    print ("Getting Eyes")

def getHeadPosition():
    print ("Getting Head Position")