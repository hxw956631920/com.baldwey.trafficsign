

import numpy as np
import matplotlib.pyplot as plt
#%matplotlib inline

#set default show params
plt.rcParams['figure.figsize'] = (10, 10)
plt.rcParams['image.interpolation'] = 'nearest'
plt.rcParams['image.cmap'] = 'gray'

import sys 
import os
import cv2

caffe_root = '/home/baldwey/caffe_git/caffe/'
sys.path.insert(0, caffe_root + '/python')

import caffe

data_root = '/home/baldwey/GTSRB/'

net = None

def binary2npy(src, dest):
    #create protobuf blob
    blob = caffe.proto.caffe_pb2.BlobProto() 
    #read mean.binaryproto
    data = open(src, 'rb').read()
    #parsing to blob
    blob.ParseFromString(data)
    #transform the mean in blob to numpy format
    array = np.array(caffe.io.blobproto_to_array(blob))
    mean_npy = array[0]
    np.save(dest, mean_npy)
    return mean_npy

def transform(path):
    mu = np.load(path)
    mu = mu.mean(1).mean(1)
    transformer = caffe.io.Transformer({'data':net.blobs['data'].data.shape})
    transformer.set_transpose('data', (2, 0, 1))
    transformer.set_mean('data', mu)
    transformer.set_raw_scale('data', 255)
    # exchange channels, from rgb to bgr
    transformer.set_channel_swap('data', (2, 1, 0))
    return transformer

def main():
    #set caffe mode is cpu
    caffe.set_mode_cpu()
    #data root
    model_def = data_root + 'model/deploy.prototxt'
    model_weights = data_root + '_iter_9000.caffemodel'
    model_mean_input = data_root + 'data/mean.binaryproto'
    model_mean_output = data_root + 'data/mean.npy'
    #init net
    global net
    net = caffe.Net(model_def, model_weights, caffe.TEST)
    #set test image's dimension is 48*49
    net.blobs['data'].reshape(1,3,48,48) 
    #transform binaryproto file to npy file
    npyfile = binary2npy(model_mean_input, model_mean_output)
    transformer = transform(model_mean_output)
    #use local img to predict
    #image = caffe.io.load_image(data_root+'Final_Test/Images/00051.ppm')
    #print("inner pic")
    #image = caffe.io.load_image(data_root+'/camera_img/1.png')
    #print("outer pic")
    #plt.imshow(image)
    #plt.show()
    image = None
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        cv2.imshow('pic', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        elif cv2.waitKey(1) & 0xFF == ord('t'):
            cv2.imwrite(data_root+"camera_img/1.png", frame)
            print("finish camera")
            image = frame
            break
    transformed_image = transformer.preprocess('data', image)
    # copy image data to net
    net.blobs['data'].data[...] = transformed_image
    # run classify
    output = net.forward()
    output_prob = output['prob'][0]
    print 'predicted class is:', output_prob.argmax()
    labels_file = data_root + 'data/val.txt'
    if os.path.exists(labels_file):
        labels = np.loadtxt(labels_file, str, delimiter='\r')
        print 'output lable:', labels[output_prob.argmax()]
    top_inds = output_prob.argsort()[::-1][:5]

    print 'probabilities and labels', zip(output_prob[top_inds], labels[top_inds])

if __name__ == '__main__':
    main()
