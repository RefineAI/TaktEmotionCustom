import caffe
import cv2
from keras.models import load_model
from EmotionDetector import setup
import numpy as np
from EmotionDetector import class_img


def getModels():
    AGE_PRETRAINED = '/home/icarus/projects/AgeGender/model/age_net.caffemodel'
    AGE_MODEL_FILE = '/home/icarus/projects/AgeGender/model/deploy_age.prototxt'

    GENDER_MODEL_FILE = '/home/icarus/projects/AgeGender/model/deploy_gender.prototxt'
    GENDER_PRETRAINED = '/home/icarus/projects/AgeGender/model/gender_net.caffemodel'

    EMOTION_MODEL_FILE = '/home/icarus/projects/AgeGender/model/deploy.prototxt'
    EMOTION_PRETRAINED = '/home/icarus/projects/AgeGender/model/ggn_full_crop_iter_56000.caffemodel'

    VGG_EMOTION_MODEL_FILE = '/home/icarus/projects/AgeGender/model/DemoDir/VGG_S_rgb/deploy.prototxt'
    VGG_EMOTION_PRETRAINED = '/home/icarus/projects/AgeGender/model/DemoDir/VGG_S_rgb/EmotiW_VGG_S.caffemodel'



    emotion_net = setup(EMOTION_MODEL_FILE, EMOTION_PRETRAINED)

    age_net = caffe.Classifier(AGE_MODEL_FILE, AGE_PRETRAINED,
                               # mean = mean,
                               # mean=np.load(caffe_root + 'python/caffe/imagenet/ilsvrc_2012_mean.npy').mean(1).mean(1),
                               channel_swap=(2, 1, 0),
                               raw_scale=255,
                               image_dims=(256, 256))

    gender_net = caffe.Classifier(GENDER_MODEL_FILE, GENDER_PRETRAINED,
                                  # mean = mean,
                                  # mean=np.load(caffe_root + 'python/caffe/imagenet/ilsvrc_2012_mean.npy').mean(1).mean(1),
                                  channel_swap=(2, 1, 0),
                                  raw_scale=255,
                                  image_dims=(256, 256))




    vgg_emotion_net = caffe.Classifier(VGG_EMOTION_MODEL_FILE, VGG_EMOTION_PRETRAINED,
                               # mean = mean,
                               #mean=np.load(caffe_root + 'python/caffe/imagenet/ilsvrc_2012_mean.npy').mean(1).mean(1),
                               channel_swap=(2, 1, 0),
                               raw_scale=255,
                               image_dims=(256, 256))

    keras_emotion_net =  load_model("../model/epoch_75.hdf5")

    facePath = "/home/icarus/projects/AgeGender/cgi-bin/haarcascade_frontalface_default.xml"
    smilePath = "/home/icarus/common-haars/haarcascade_smile.xml"
    faceCascade = cv2.CascadeClassifier(facePath)
    smileCascade = cv2.CascadeClassifier(smilePath)

    nets = {}
    nets['age'] = age_net
    nets['gender'] = gender_net
    nets['emotion'] = emotion_net
    nets['faceCascade'] = faceCascade
    nets['smileCascade'] = smileCascade
    nets['vgg'] = vgg_emotion_net
    nets["keras_emo"] = keras_emotion_net
    return nets




