from xml.dom import minidom
import pickle
import os
from os import listdir, getcwd
from os.path import join
import re

sets=[('2007', 'train'), ('2007', 'val'), ('2007', 'test')]

classes = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19",
            "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31", "32", "33", "34", "35", "36", "37", "38", "39", 
            "40", "41", "42"]


def convert(size, box):
    dw = 1./size[0]
    dh = 1./size[1]
    x = (box[0] + box[1])/2.0
    y = (box[2] + box[3])/2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)

def convert_annotation(year, image_id):
    xmlfileName = 'VOCdevkit/VOC%s/Annotations/%s.xml'%(year, image_id)
    print(xmlfileName)
    if os.path.exists(xmlfileName):
        in_file = open(xmlfileName)
        out_file = open('VOCdevkit/VOC%s/labels/%s.txt'%(year, image_id), 'w')
        dom = minidom.parse(in_file)
        root = dom.documentElement
        sizeTag = root.getElementsByTagName('size')[0]
        widthTag = sizeTag.getElementsByTagName('width')[0]
        heightTag = sizeTag.getElementsByTagName('height')[0]
        width = widthTag.childNodes[0].data
        height = heightTag.childNodes[0].data

        objectTag = root.getElementsByTagName('object')[0]
        nameTag = objectTag.getElementsByTagName('name')[0]
        name = nameTag.childNodes[0].data
        
        difficulTag = objectTag.getElementsByTagName('difficult')[0]
        difficult = difficulTag.childNodes[0].data
        if name not in classes or int(difficult) == 1:
            return
        name_id = classes.index(name)

        bndboxTag = objectTag.getElementsByTagName('bndbox')[0]
        xminTag = bndboxTag.getElementsByTagName('xmin')[0]
        xmin = xminTag.childNodes[0].data
        yminTag = bndboxTag.getElementsByTagName('ymin')[0]
        ymin = yminTag.childNodes[0].data
        xmaxTag = bndboxTag.getElementsByTagName('xmax')[0]
        xmax = xmaxTag.childNodes[0].data
        ymaxTag = bndboxTag.getElementsByTagName('ymax')[0]
        ymax = ymaxTag.childNodes[0].data
        box = (float(xmin), float(ymin), float(xmax), float(ymax))
        bb = convert((float(width), float(height)), box)
        out_file.write(str(name_id) + " " + " ".join([str(a) for a in bb]) + '\n')
    # tree=ET.parse(in_file)
    # root = tree.getroot()
    # size = root.find('size')
    # w = int(size.find('width').text)
    # h = int(size.find('height').text)

    # for obj in root.iter('object'):
    #     difficult = obj.find('difficult').text
    #     cls = obj.find('name').text
    #     if cls not in classes or int(difficult) == 1:
    #         continue
    #     cls_id = classes.index(cls)
    #     xmlbox = obj.find('bndbox')
    #     b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
    #     bb = convert((w,h), b)
    #     out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')

wd = getcwd()

for year, image_set in sets:
    # VOCdevkit/VOC2007/labels/
    if not os.path.exists('VOCdevkit/VOC%s/labels/'%(year)):
        os.makedirs('VOCdevkit/VOC%s/labels/'%(year))
    # VOCdevkit/VOC2007/ImageSets/Main/train.txt
    image_ids = open('VOCdevkit/VOC%s/ImageSets/Main/%s.txt'%(year, image_set)).read().strip().split()
    list_file = open('%s_%s.txt'%(year, image_set), 'w')
    for image_id in image_ids:
        roots = image_id.split('/')
        if not os.path.exists('VOCdevkit/VOC%s/labels/'%(year)+roots[0]):
            os.makedirs('VOCdevkit/VOC%s/labels/'%(year)+roots[0])
        list_file.write('%s/VOCdevkit/VOC%s/JPEGImages/%s.ppm\n'%(wd, year, image_id))
        convert_annotation(year, image_id)
    list_file.close()

