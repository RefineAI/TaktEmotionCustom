#!/home/icarus/anaconda2/bin/python
import cgitb; cgitb.enable()
import collections
import time
import cv2
from videoUtils  import getFaces,  getSmiles, getHeadPosition, getEyes
#from DynamoDB import insertTable
from TaktUtils import objToStr
#from MsTaktUtil import objToStr
import cgi
from AgeGenderDetector import predictMetrics, predictMetricsWithMicrosoft
from AWSFetchData import getImages
from TaktUtils import read64

#TEMP_FRAME_STORE = "/home/icarus/projects/AgeGender/tmp/"

TEMP_FRAME_STORE = "/home/icarus/projects/AgeGender/cgi-bin/static/"


def appendResults(dirID, result):
    with open(dirID + ".json", "a") as resultFile:
        resultFile.write(result)

def get_emotion(nets, data, companyId, videoId, userId, timestamp, cache):
    print ("In get Emotion [Driver.py]")
    skip =["companyId","campaignId", "participantId"]
    orderedData = collections.OrderedDict(sorted(data.items()))
    result = ""
    try:
        for key in orderedData:
            if (key in skip):
                continue
            f = data[key]
            frame = read64(f)
            if (frame is "Error"):
                print ("Error in decoding base64")
                continue
            img_name = str(userId) + ".jpeg"
            path = TEMP_FRAME_STORE + img_name
            #print ("saving image to + " + path + "[Driver.py]")
            cv2.imwrite(path, frame)

            # print "Created image: "  + path
            ####### Change this to swap models
            result = analyze_data(nets, path, companyId, videoId, userId, timestamp, cache)
            #result = analyze_data_microsoft(nets, path, companyId, videoId, userId, timestamp, cache)
    except cv2.error as e:
        print ("CV2 Error: " + str(e) )
    return result

def get_emotion_image(nets, path, companyId, videoId, userId,  timestamp , cache):
    emotions = {}
    emotions['userId'] = userId
    emotions['videoId'] = videoId
    emotions['report'] = []
    result = analyze_data(nets, path, companyId,  videoId, userId, timestamp, cache)
    return result


def analyze_data_microsoft(nets, path, companyId, videoId, userId, timestamp, cache):
    print ("In Analyze In MS Service")
    emotions = []
    results = predictMetricsWithMicrosoft(None, path, None, None, None)
    metricsHash = objToStr(results, timestamp, companyId, videoId, userId)
    emotions.append(metricsHash)
    jsonStr = "["
    for i in emotions:
        jsonStr = jsonStr + str(i)
    jsonStr = jsonStr + "]"
    # print jsonStr
    return jsonStr


def analyze_data(nets, path,  companyId, videoId, userId, timestamp, cache):
    #print "In Analyze Image [Driver.py]"
    print (path)
    emotions = []
    s = time.time()
    color_frame = cv2.imread(path)
    #print "Image Size shape is: " + str(color_frame.shape)
    gray_frame = cv2.cvtColor(color_frame, cv2.COLOR_BGR2GRAY)
    faces = getFaces(gray_frame, nets["faceCascade"])  #videoUtils.py
    if(len(faces) > 0):
        for (x, y, w, h) in faces:
            #print "Face Found"
            count = len(faces)
            roi_gray = gray_frame[y:y + h, x:x + w]
            roi_color = color_frame[y:y + h, x:x + w]
            #smileFound = getSmiles(roi_gray, count, nets["smileCascade"])

            tmp_color_frame = color_frame / 255.
            cropped_face_in_color = tmp_color_frame[:, :, (2, 1, 0)]
            sub_face_in_color = cropped_face_in_color[y:y + h, x:x + w]

            smallsize = (227, 227)

            resized_face_in_color = cv2.resize(sub_face_in_color, smallsize)
            ####### Change this to swap models
            results = predictMetrics(resized_face_in_color, path, nets, cache, userId ) #AgeGenderDetector.py
            #results = predictMetricsWithMicrosoft(resized_face_in_color, path, nets, cache, userId)

            metricsHash = objToStr(results, timestamp, companyId, videoId, userId) #TaktUtils.py
            emotions.append(metricsHash)
            print (results["class"])

            #print str("*******") + str(results)
            text = ""
            #if (not smileFound):
            #    text = results["class"]
            #else:
            #    text = "Happiness"
            #cv2.rectangle(color_frame, (x, y), (x + w, y + h), (255, 0, 0))
            #font = cv2.FONT_HERSHEY_SIMPLEX
            #cv2.putText(color_frame, text, (x, y + 10), font, 1, (255, 0, 0), 2)
            #cv2.imwrite(path, color_frame)
            break
    else:
            print ("No faces found [Driver.py]")
            metricsHash = objToStr(None, timestamp, companyId, videoId, userId)
            emotions.append(metricsHash)
    e = time.time()
    #print "Entire operation took: " + str(e - s) + "!!! [Driver.py]"
    jsonStr = "["
    for i in emotions:
        jsonStr = jsonStr + str(i)
    jsonStr = jsonStr + "]"
    #print jsonStr
    return jsonStr


def saveToDB(jsonData):
    print ("Saving results to DB")
    insertTable(jsonData)

def find_faces(image):
    #faces_coordinates = _locate_faces(image)
    #cutted_faces = [image[y:y + h, x:x + w] for (x, y, w, h) in faces_coordinates]
    #normalized_faces = [_normalize_face(face) for face in cutted_faces]
    #return zip(normalized_faces, faces_coordinates)
    return

def _normalize_face(face):
    face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
    face = cv2.resize(face, (350, 350))
    return face;

'''def _locate_faces(image):
    faces = faceCascade.detectMultiScale(
        image,
        scaleFactor=1.1,
        minNeighbors=15,
        minSize=(70, 70)
    )'''


if __name__=="__main__":
    args = cgi.FieldStorage()
    action = None
    fileId = None
    if args.has_key("companyId"):
        companyId = args["companyId"].value
    if args.has_key("participantId"):
        participantId = args["participantId"].value
    if args.has_key("campaignId"):
        campaignId = args["campaignId"].value

    data = getImages(companyId, campaignId, participantId)
    data['participantId'] = participantId
    data['companyId'] = companyId
    data['campaignId'] = campaignId
    response = get_emotion(data, companyId, participantId, campaignId)
    saveToDB(response)
    print ('''Content-type: text/html

       ''')
    print ("done!")



