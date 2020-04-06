#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import random


trainval_percent = 0.1
train_percent = 0.9

xmldirpath = './VOC2007/Annotations'
txtsavepath = './VOC2007/ImageSets/Main'
total_xmldir = os.listdir(xmldirpath)

# 打开文件
ftrainval = open('./VOC2007/ImageSets/Main/trainval.txt', 'a')
ftest = open('./VOC2007/ImageSets/Main/test.txt', 'a')
ftrain = open('./VOC2007/ImageSets/Main/train.txt', 'a')
fval = open('./VOC2007/ImageSets/Main/val.txt', 'a')
print(total_xmldir)
# 遍历目录
for dirs in total_xmldir:
    print('./VOC2007/Annotations/'+dirs)
    # 每个目录下所有的xml文件
    total_xml = os.listdir('./VOC2007/Annotations'+'/'+dirs)

    num = len(total_xml)
    list = range(num)
    tv = int(num * trainval_percent)
    tr = int(tv * train_percent)
    trainval = random.sample(list, tv)
    train = random.sample(trainval, tr)
    for i in list:
        name = total_xml[i][:-4] + '.jpg' + '\n'
        if i in trainval:
            ftrainval.write('./VOC2007/JPEGImages/'+dirs+'/'+name)
            if i in train:
                ftest.write('./VOC2007/JPEGImages/'+dirs+'/'+name)
            else:
                fval.write('./VOC2007VOC2007/JPEGImages/'+dirs+'/'+name)
        else:
            ftrain.write('./VOC2007/JPEGImages/'+dirs+'/'+name)

ftrainval.close()
ftrain.close()
fval.close()
ftest.close()