#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import random

path = sys.argv[1]

trainval_percent = 0.1
train_percent = 0.9

xmldirpath = path+'/Annotations'
txtsavepath = path+'/ImageSets/Main'
total_xmldir = os.listdir(xmldirpath)

# 打开文件
ftrainval = open(path+'/ImageSets/Main/trainval.txt', 'a')
ftest = open(path+'/ImageSets/Main/test.txt', 'a')
ftrain = open(path+'/ImageSets/Main/train.txt', 'a')
fval = open(path+'/ImageSets/Main/val.txt', 'a')
print(total_xmldir)
# 遍历目录
for dirs in total_xmldir:
    print(path+'/Annotations'+'/'+dirs)
    # 每个目录下所有的xml文件
    total_xml = os.listdir(path+'/Annotations'+'/'+dirs)

    num = len(total_xml)
    list = range(num)
    tv = int(num * trainval_percent)
    tr = int(tv * train_percent)
    trainval = random.sample(list, tv)
    train = random.sample(trainval, tr)
    for i in list:
        name = total_xml[i][:-4] + '.jpg' + '\n'
        if i in trainval:
            ftrainval.write(dirs+'/'+name)
            if i in train:
                ftest.write(dirs+'/'+name)
            else:
                fval.write(dirs+'/'+name)
        else:
            ftrain.write(dirs+'/'+name)

ftrainval.close()
ftrain.close()
fval.close()
ftest.close()