

#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
from PIL import Image
import re

path = sys.argv[1]

for root, dirs, files in os.walk(path):
    for file in files:
        filepath = os.path.join(root, file)
        if os.path.isfile(filepath) and re.match(u".*(ppm)+$", filepath):
            fileName = filepath[:-4]+".jpg"
            img = Image.open(filepath) 
            print(fileName)
            img.save(fileName)
            os.remove(filepath)
