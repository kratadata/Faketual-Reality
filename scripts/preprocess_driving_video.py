'''
This script is needed to preprocess all the driving videos (if needed) cropping the faces and resizing them to 512.
'''

import os
import subprocess

#put all the videos in a folder, and preprocess all of them
rootdir = '/home/paulina/Desktop/driving_videos/finish'
outdir = (os.path.join(rootdir, 'cropped'))
if not os.path.exists(outdir):
    os.mkdir(outdir)

cmd = ["python", "./crop-video.py","--inpdir", rootdir]
subprocess.Popen(cmd).wait()
