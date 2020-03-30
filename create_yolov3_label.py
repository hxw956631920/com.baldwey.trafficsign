#!/usr/bin/python
# -*- coding: utf-8 -*-

import csv  
import codecs
import sys
import re
import os

#造一个类来做数据存储 该类为gtsrb提供的xlms文件中的格式 还需转换为yolo3能的标签格式
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

# yolo3的标签格式
class yolo3Data:
    def __init__(self):
        # 框选区域宽度
        self.width = 0
        # 框选区域高度
        self.height = 0
        # 框选区域中心点x
        self.x = 0
        # 框选区域中心点y
        self.y = 0
        # 对应标签
        self.label = 0
        # 转换为存储在.txt中的数据
        self.data = ""
yolo3 = yolo3Data()

# gtsrb格式转为yolo3格式
def gtsrbToyolo3():
    yolo3.width = (gtsrb.x2 - gtsrb.x1)/gtsrb.width
    yolo3.height = (gtsrb.y2 - gtsrb.y1)/gtsrb.height
    yolo3.x = ((gtsrb.x2 - gtsrb.x1)/2 + gtsrb.x1)/gtsrb.width
    yolo3.y = ((gtsrb.y2 - gtsrb.y1)/2 + gtsrb.y1)/gtsrb.height
    yolo3.label = gtsrb.label

# 获取gtsrb数据
def getGtsrbData(result):
        gtsrb.filename = result[0]
        gtsrb.width = float(result[1])
        gtsrb.height = float(result[2])
        gtsrb.x1 = float(result[3])
        gtsrb.y1 = float(result[4])
        gtsrb.x2 = float(result[5])
        gtsrb.y2 = float(result[6])
        gtsrb.label = int(result[7])

# 获取数据
def dealData(workbook):
    index = 0
    #遍历行取数据
    for row in workbook:
        if index == 0:
            index+=1
            continue
        else:    
            result = re.split(r';', row[0])
            getGtsrbData(result)
            gtsrbToyolo3()
            yolo3.data += str(yolo3.label) + " " + str(yolo3.x) + " " + str(yolo3.y) + " " + str(yolo3.width) + " " + str(yolo3.height) + "\n"
            index += 1
            





# 处理文件夹下所有的标签
def findExcel(path):
    for root, dirs, files in os.walk(path):
        for file in files:
            filepath = os.path.join(root, file)
            if os.path.isfile(filepath) and re.match(u".*(csv)+$", filepath):
                print(filepath)
                # 打开excel
                with open(filepath, 'r') as f:
                    workbook = csv.reader(f)
                    dealData(workbook)
                    finish_output(path)

#输出文件
def finish_output(path):
    dirpath = os.path.dirname(path)
    #写入文件，用codecs来做，回避编码问题
    output = codecs.open(dirpath + "/fileList.txt", 'w', encoding='utf-8')
    output.write(yolo3.data)
    output.close()
    print("Export finish, see " + dirpath + "/fileList.txt")

def main():
    path = sys.argv[1]
    findExcel(path)
        
    



if __name__ == '__main__':
    main()
