'''
script to check the dimensions of a video
'''

path = '/project/PycharmProjects/ma-thesis-alessia-paccagnella/data/vox'
import os
import sys
import glob
import subprocess
import shutil
import cv2

subdirs = [x[0] for x in os.walk(path)] #train, test
for i in subdirs:
    os.chdir(i)
    print(i)
    for file in os.listdir(i):
        vcap = cv2.VideoCapture(file)

        if vcap.isOpened():
            width = vcap.get(cv2.CAP_PROP_FRAME_WIDTH)  # float
            height = vcap.get(cv2.CAP_PROP_FRAME_HEIGHT)  # float

            width = vcap.get(3)  # float
            height = vcap.get(4)  # float
            if (width != 512) or (height != 512):
                print(i, file, 'width, height:', width, height)

