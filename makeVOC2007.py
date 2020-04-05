#!/usr/bin/python
# -*- coding: utf-8 -*-

import csv  
import codecs
import sys
import re
import os
# 导入dom访问xml
from xml.dom.minidom import Document
# 汉字报错处理，统一成utf-8
reload(sys)
sys.setdefaultencoding('utf-8')


class gtsrbData:
    def __init__(self):
        # 图片名字
        self.filename = 0
        # 图片宽度
        self.width = 0
        # 图片高度
        self.height = 0
        # 框选起点x
        self.x1 = 0
        # 框选起点y
        self.y1 = 0
        # 框选终点x
        self.x2 = 0
        # 框选终点y
        self.y2 = 0
        # 对应标签
        self.label = 0
gtsrb = gtsrbData()

# 获取gtsrb数据
def getGtsrbData(result):
        gtsrb.filename = result[0]
        gtsrb.width = result[1]
        gtsrb.height = result[2]
        gtsrb.x1 = result[3]
        gtsrb.y1 = result[4]
        gtsrb.x2 = result[5]
        gtsrb.y2 = result[6]
        gtsrb.label = result[7]

# 获取数据
def dealData(workbook, path):
    index = 1
    #遍历行取数据
    for row in workbook:
        print(index)   
        result = re.split(r';', row[0])
        getGtsrbData(result)
        # 创建对应xml文件
        makeXML(path)
        index+=1


# 处理所有excel表
def findExcel(path):
    for root, dirs, files in os.walk(path):
        for file in files:
            filepath = os.path.join(root, file)
            if os.path.isfile(filepath) and re.match(u".*(csv)+$", filepath):
                with codecs.open(filepath, 'rb') as f:
                    workbook = csv.reader(line.replace('\0', '') for line in f)
                    workbook.next()
                    dealData(workbook, root)




# 遍历Images所在的所有的文件夹及其子文件夹，并在Images_label创建对应目录
def check_make_dir(path):
    for root, dirs, files in os.walk(path):
        for d in dirs:
            newdir = os.path.join(root, d)
            sub = re.sub(r'/JPEGImages/', '/Annotations/', newdir)
            if not os.path.exists(sub):
                os.mkdir(sub)

# 生成对应xml文件
def makeXML(filePath):
    # 创建dom文档对象
    doc = Document()
    annotation = doc.createElement('annotation')
    doc.appendChild(annotation)

    folder = doc.createElement('folder')
    annotation.appendChild(folder)
    folder_text = doc.createTextNode('JPEGImages') #元素内容写入
    folder.appendChild(folder_text)

    filename = doc.createElement('filename')
    annotation.appendChild(filename)
    filename_text = doc.createTextNode(gtsrb.filename) #元素内容写入
    filename.appendChild(filename_text)

    path = doc.createElement('path')
    annotation.appendChild(path)
    path_text = doc.createTextNode('Unkown') #元素内容写入
    path.appendChild(path_text)

    source = doc.createElement('source')
    annotation.appendChild(source)
    
    database = doc.createElement('database')
    source.appendChild(database)
    database_text = doc.createTextNode('Unkown') #元素内容写入
    database.appendChild(database_text)

    size = doc.createElement('size')
    annotation.appendChild(size)

    width = doc.createElement('width')
    size.appendChild(width)
    width_text = doc.createTextNode(gtsrb.width) #元素内容写入
    width.appendChild(width_text) 

    height = doc.createElement('height')
    size.appendChild(height)
    height_text = doc.createTextNode(gtsrb.height) #元素内容写入
    height.appendChild(height_text)  

    depth = doc.createElement('depth')
    size.appendChild(depth)
    depth_text = doc.createTextNode('3') #元素内容写入
    depth.appendChild(depth_text)  

    segmented = doc.createElement('segmented')
    annotation.appendChild(segmented)
    segmented_text = doc.createTextNode('0') #元素内容写入
    segmented.appendChild(segmented_text)  

    objects = doc.createElement('object')
    annotation.appendChild(objects) 

    name = doc.createElement('name')
    objects.appendChild(name)
    name_text = doc.createTextNode(gtsrb.label) #元素内容写入
    name.appendChild(name_text)  

    pose = doc.createElement('pose')
    objects.appendChild(name)
    pose_text = doc.createTextNode('Unspecified') #元素内容写入
    pose.appendChild(pose_text)    

    truncated = doc.createElement('truncated')
    objects.appendChild(truncated)
    truncated_text = doc.createTextNode('0') #元素内容写入
    truncated.appendChild(truncated_text)     

    difficult = doc.createElement('difficult')
    objects.appendChild(difficult)
    difficult_text = doc.createTextNode('0') #元素内容写入
    difficult.appendChild(difficult_text)

    bndbox = doc.createElement('bndbox')
    objects.appendChild(bndbox) 

    xmin = doc.createElement('xmin')
    bndbox.appendChild(xmin)
    xmin_text = doc.createTextNode(gtsrb.x1) #元素内容写入
    xmin.appendChild(xmin_text)       

    ymin = doc.createElement('ymin')
    bndbox.appendChild(ymin)
    ymin_text = doc.createTextNode(gtsrb.y1) #元素内容写入
    ymin.appendChild(ymin_text)       

    xmax = doc.createElement('xmax')
    bndbox.appendChild(xmax)
    xmax_text = doc.createTextNode(gtsrb.x2) #元素内容写入
    xmax.appendChild(xmax_text)       

    ymax = doc.createElement('ymax')
    bndbox.appendChild(ymax)
    ymax_text = doc.createTextNode(gtsrb.y2) #元素内容写入
    ymax.appendChild(ymax_text)     

    sub = re.sub(r'.ppm', '.xml', gtsrb.filename)
    newpath = re.sub(r'/JPEGImages/', '/Annotations/', filePath)
    gtsrb.filename
    xmlFile = open(newpath+'/'+sub, 'w')
    doc.writexml(xmlFile, indent = '', newl='\n', addindent = '\t')
    xmlFile.close()        

def main():
    path = sys.argv[1]
    check_make_dir(path)
    findExcel(path)
        
if __name__ == '__main__':
    main()