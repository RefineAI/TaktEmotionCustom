#!/home/icarus/anaconda2/bin/python
import numpy as np
#import matplotlib.pyplot as plt
import json
import caffe

import csv

import sys
import os

caffe_root = '/home/icarus/installs/caffe/'
sys.path.insert(0, caffe_root + 'python')


caffe.set_mode_gpu()
caffe.set_device(0)




# set the size of the input (we can skip this if we're happy
#  with the default; we can also change it later, e.g., for different batch sizes)
def setup(model_def, model_weights):
    print ("In EmotionDetector Setup!!")
    global net
    global transformer


    net = caffe.Net(model_def,      # defines the structure of the model
                    model_weights,  # contains the trained weights
                    caffe.TEST)     # use test mode (e.g., don't perform dropout)

    mu = np.array([127,127,127])

    # create transformer for the input called 'data'
    transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})

    transformer.set_transpose('data', (2,0,1))  # move image channels to outermost dimension
    transformer.set_mean('data', mu)            # subtract the dataset-mean value in each channel
    transformer.set_raw_scale('data', 255)      # rescale from [0, 1] to [0, 255]
    transformer.set_channel_swap('data', (2,1,0))  # swap channels from RGB to BGR
    net.blobs['data'].reshape(50,        # batch size
                              3,         # 3-channel (BGR) images
                              227, 227)  # image size is 227x227
    return net

def defaults():
    setup('ggn-net/deploy.prototxt', 'snapshots/ggn_full_crop_halfface_iter_56000.caffemodel')


cursize = 50
def resize(ournet, size, oldsize):
    if oldsize != size:
        ournet.blobs['data'].reshape(size, 3, 227, 227)
        cursize = size

def class_img(img, emotion_net):
    caffe.set_mode_gpu()
    caffe.set_device(0)
    image = img
    #resize(net, 1, cursize)
    resize(emotion_net, 1, cursize)
    print ("Image to predict is : " + str(img) )
    #if isinstance(img, str):
    #   print "Loading from file..."
    image = caffe.io.load_image(img) #commented by Rafi for testing
    #else:
    #    print "Loading from CV2 matrix..."
     #   image = img

    transformed_image = transformer.preprocess('data', image)
    #plt.imshow(image)
    # copy the image data into the memory allocated for the net
    emotion_net.blobs['data'].data[0] = transformed_image
    ### perform classification
    output = emotion_net.forward()

    #print "Output is: " + str(output)

    output_prob = output['prob'][0]  # the output probability vector for the first image in the batch

    #print output_prob
    #return output_prob.argmax()
    #print 'predicted class is:', output_prob.argmax()
    #return json.dumps({"class": output_prob.argmax(), "output_prob": output_prob.tolist()})
    return output_prob

def class_imgs(list_img):
    """
    Classify all images in a python list
    Keyword arguements:
    list_img -- List of files relative to the current working directory
    """
    numberimg = len(list_img)
    resize(net, numberimg, cursize)
    i = 0
    for img in list_img:
        image = caffe.io.load_image(img)
        transformed_image = transformer.preprocess('data', image)
        net.blobs['data'].data[i] = transformed_image
        i = i + 1

    output = net.forward()

    results = []
    for n in range(0, numberimg):
        themax = output['prob'][n].argmax()
        results.append({'filename':list_img[n], 'class': themax, 'prob': output['prob'][n].tolist()})

    return results

if __name__=="__main__":
    print ("Loading Emotion Module")


