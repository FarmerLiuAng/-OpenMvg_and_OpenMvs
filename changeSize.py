import os
from PIL import Image
import re

path_1 = "/mnt/md0/liuang/mvs/data_main/shoubing_half/images/"
width_new = 2016
height_new = 1134
list = os.listdir(path_1)
for file in list:
    path_2 = path_1+file
    #print(path_2)
    im = Image.open(path_2)
    w,h = im.size
    #print(w,h)
    out = im.resize((width_new,height_new),Image.ANTIALIAS)
    out.save(path_2)
    