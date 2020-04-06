#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from os import listdir, getcwd
import sys
import random

wd = getcwd()

trainval_percent = 0.1
train_percent = 0.9

xmldirpath = '%s/VOC2007/Annotations'%(wd)
txtsavepath = '%s/VOC2007/ImageSets/Main'%(wd)
total_xmldir = os.listdir(xmldirpath)

# 打开文件
ftrainval = open('%s/VOC2007/ImageSets/Main/trainval.txt'%(wd), 'a')
ftest = open('%s/VOC2007/ImageSets/Main/test.txt'%(wd), 'a')
ftrain = open('%s/VOC2007/ImageSets/Main/train.txt'%(wd), 'a')
fval = open('%s/VOC2007/ImageSets/Main/val.txt'%(wd), 'a')
print(total_xmldir)
# 遍历目录
for dirs in total_xmldir:
    print('%s/VOC2007/Annotations/'%(wd)+dirs)
    # 每个目录下所有的xml文件
    total_xml = os.listdir('%s/VOC2007/Annotations'%(wd)+'/'+dirs)

    num = len(total_xml)
    list = range(num)
    tv = int(num * trainval_percent)
    tr = int(tv * train_percent)
    trainval = random.sample(list, tv)
    train = random.sample(trainval, tr)
    for i in list:
        name = total_xml[i][:-4] + '.jpg' + '\n'
        if i in trainval:
            ftrainval.write('%s/VOC2007/JPEGImages/'%(wd)+dirs+'/'+name)
            if i in train:
                ftest.write('%s/VOC2007/JPEGImages/'%(wd)+dirs+'/'+name)
            else:
                fval.write('%s/VOC2007VOC2007/JPEGImages/'%(wd)+dirs+'/'+name)
        else:
            ftrain.write('%s/VOC2007/JPEGImages/'%(wd)+dirs+'/'+name)

ftrainval.close()
ftrain.close()
fval.close()
ftest.close()