#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
#%matplotlib inline


import sys 
import os
import cv2
import caffe
from PIL import Image

data_root = '/home/baldwey/GTSRB/'

#设置默认参数 设置caffe根目录路径
plt.rcParams['figure.figsize'] = (10, 10)
plt.rcParams['image.interpolation'] = 'nearest'
plt.rcParams['image.cmap'] = 'gray'
caffe_root = '/home/baldwey/caffe_git/caffe/'

sys.path.insert(0, caffe_root + '/python')

net = None

def ifnil(t, default):
    if t == None:
        t = default

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

def transform(path, net):
    mu = np.load(path)
    mu = mu.mean(1).mean(1)
    transformer = caffe.io.Transformer({'data':net.blobs['data'].data.shape})
    transformer.set_transpose('data', (2, 0, 1))
    transformer.set_mean('data', mu)
    transformer.set_raw_scale('data', 255)
    # exchange channels, from rgb to bgr
    transformer.set_channel_swap('data', (2, 1, 0))
    return transformer

def camera():
    # 初始化摄像头
    cap = cv2.VideoCapture(0)
    # 循环拍照读取
    while True:
        ret, frame = cap.read()
        cv2.imshow('pic', frame)
        # 按键盘q键退出
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        # 按键盘t键拍照
        elif cv2.waitKey(1) & 0xFF == ord('t'):
            cv2.imwrite(data_root+"camera_img/1.png", frame)
            print("take picture finish")
            break

def run(picPath, width = None, height = None):
    # 设置cpu模式
    caffe.set_mode_cpu()
    # 测试模型
    model_def = data_root + 'model/deploy.prototxt'
    # 权重
    model_weights = data_root + '_iter_9000.caffemodel'
    # mean.binaryproto的路径
    model_mean_input = data_root + 'data/mean.binaryproto'
    # 转换为.npy的输出路径
    model_mean_output = data_root + 'data/mean.npy'
    # 转换binaryproto 文件为 npy文件 如果转换过则跳过这一步
    if os.path.exists(model_mean_output):
       npyfile = binary2npy(model_mean_input, model_mean_output)
       print("#########binaryproto file to npyfile finish#######")
    # 初始化网络
    net = caffe.Net(model_def, model_weights, caffe.TEST)
    # 读取图片
    # image = Image.open(picPath)#返回一个Image对象
    image = caffe.io.load_image(data_root+picPath)
    # 获取图片尺寸
    width = image.size[0]
    height = image.size[1]
    # 设置输入图片大小
    ifnil(width, 48)
    ifnil(height, 48)
    # 设置数据读取层的形状
    net.blobs['data'].reshape(1,3,width,height) 
    # 均值处理过的结果
    # transformer = transform(model_mean_output, net)
    # 显示图片
    plt.imshow(image)
    plt.show()
    # # 对图片进行去均值处理
    # transformed_image = transformer.preprocess('data', image)
    # # 拷贝图像数据到网络层
    # net.blobs['data'].data[...] = transformed_image
    # # 前向传播计算得到结果
    # output = net.forward()
    # # 从softmax层在该模型中命名为prob 将结果取出
    # output_prob = output['prob'][0]
    # # 打印结果
    # print 'predicted class is:', output_prob.argmax()
    # # 对比标签文件中其它5个高可能性的结果
    # labels_file = data_root + 'data/val.txt'
    # if os.path.exists(labels_file):
    #     labels = np.loadtxt(labels_file, str, delimiter='\r')
    #     print 'output lable:', labels[output_prob.argmax()]
    # top_inds = output_prob.argsort()[::-1][:5]
    # print 'probabilities and labels', zip(output_prob[top_inds], labels[top_inds])

# 参数1 flag 模式： 模式1 图片模式 模式2 摄像头模式
# 参数2 picPath 图片地址 (图片模式为图片所在地址 摄像头模式为摄像头保存的图片地址)
def main():  
    run("Final_Test/Images/00002.ppm")
    # if len(sys.argv)<=3:
    #     if len():
    #         pass
    




if __name__ == '__main__':
    main()
