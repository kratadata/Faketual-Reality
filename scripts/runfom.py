'''
Script to automatically generate animation in several folders
'''

import os
from os import listdir
import subprocess
import sys


rootdir = '/local/home/apaccagne/Desktop/Drivingvideos/videos'
for root, dirs, files in os.walk(rootdir):
   for name in dirs:
       print(name)
       if (name == '6_good'): #!= 'driving' and name != 'original_driving'):# name == '6_good'):  and name != '3_turningface' and name != '4_handsproblem' and name != '1_turningface' and name != '5_problemrelativepose' ): #and name != '2_medium'):
           print(name)
           pre = os.path.join(root, name)
           name_folder = os.path.join(root, name, 'driving') #provo con ind
           print(name_folder)
           name_video = (os.listdir(name_folder))[0]
           print(name_video)

           inp = (os.path.join(name_folder, name_video))
           # print(inp)

           res_256 = inp
           output_folder = '/local/home/apaccagne/Desktop/Drivingvideos/imgs/Jelleteeth.jpg'
           print(inp)

           # Run demo of first order model with all the input images (frame) and the cropped videos

           res = os.path.join(pre, 'jelle_vecchiocheck_teeth_new_relativepose.mp4')
           cmd = ["python",
                  "./demo.py",
                  "--config", "config/vox-512.yaml",
                  "--driving_video", res_256,
                  "--source_image", output_folder,
                  "--checkpoint", "checkpoints/ciaoavanzato.pth.tar", #"log/training_png_dacheckpoint256/checkpoint.pth.tar",
                  "--relative",
                  "--adapt_scale",
                  "--result_video", res]
           subprocess.Popen(cmd).wait()





'''
name_folder = '/local/home/apaccagne/Desktop/Drivingvideos/videos/7_good/driving'
name_video = (os.listdir(name_folder))[0]
print(name_video)

inp = (os.path.join(name_folder, name_video))

res_256 = inp
output_folder = '/local/home/apaccagne/Desktop/Drivingvideos/imgs/Jelle.jpg'
print(inp)'''

'''
Run demo of first order model with all the input images (frame) and the cropped videos
'''
'''res = os.path.join('/local/home/apaccagne/Desktop/Drivingvideos/videos/7_good', 'jelle_relativepose_new.mp4')
cmd = ["python",
        "./demo.py",
        "--config", "config/vox-512.yaml",
        "--driving_video", res_256,
        "--source_image", output_folder,
        "--checkpoint", "checkpoints/ciaoavanzato.pth.tar",
        "--relative",
        "--adapt_scale",
        "--result_video", res]
subprocess.Popen(cmd).wait()'''

