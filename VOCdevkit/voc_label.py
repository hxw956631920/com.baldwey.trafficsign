from xml.dom import minidom
import pickle
import os
from os import listdir, getcwd
from os.path import join
import re
import sys

sets=[('2007', 'train'), ('2007', 'val'), ('2007', 'test')]

classes = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19",
            "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31", "32", "33", "34", "35", "36", "37", "38", "39", 
            "40", "41", "42"]

# 56 52 6 5 51 46
def convert(size, box):
    dw = 1./size[0] #1/56  
    dh = 1./size[1] #1/52
    x = (box[0] + box[1])/2.0 #1/56
    y = (box[2] + box[3])/2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)

def convert_annotation(image_id):
    xmlfileName = re.sub(r'/JPEGImages/', '/Annotations/', image_id)
    xmlfileName = xmlfileName + ".xml"
    print(xmlfileName)
    if os.path.exists(xmlfileName):
        in_file = open(xmlfileName)
        sub = re.sub(r'/JPEGImages/', '/labels/', image_id)
        out_file = open(sub+".txt", 'w')
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
        box = (float(xmin), float(xmax), float(ymin), float(ymax))
        bb = convert((float(width), float(height)), box)
        out_file.write(str(name_id) + " " + " ".join([str(a) for a in bb]) + '\n')

wd = getcwd()

for year, image_set in sets:
    if not os.path.exists('%s/VOC%s/labels/'%(wd, year)):
        os.makedirs('%s/VOC%s/labels/'%(wd, year))
    image_ids = open('%s/VOC%s/ImageSets/Main/%s.txt'%(wd, year, image_set)).read().strip().split()
    list_file = open('%s/%s_%s.txt'%(wd, year, image_set), 'w')
    for image_id in image_ids:
        roots = image_id.split('/')
        if not os.path.exists('%s/VOC%s/labels/'%(wd, year)+roots[-2]):
            os.makedirs('%s/VOC%s/labels/'%(wd, year)+roots[-2])
        list_file.write('%s\n'%(image_id))
        convert_annotation(image_id[:-4])
    list_file.close()

