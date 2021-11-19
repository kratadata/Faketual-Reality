'''
This script is needed to generate the new dataset for TecoGAN starting from a single HD video. 
'''

import os
from os import listdir
import subprocess
import sys

'''
Step 1: crop all the HR videos to 256 and to 1024
'''
rootdir = '/media/apaccagne/hdd1/video_per_tecogan_esperimento_NODFD/'
for root, dirs, files in os.walk(rootdir):
   for name in dirs:
      name_folder = os.path.join(root, name)
      name_video = next(os.path.join(name_folder, f) for f in os.listdir(name_folder) if os.path.isfile(os.path.join(name_folder, f))) #(listdir(name_folder)
      print(name_folder, name_video)
      inp = os.path.join(name_folder, name_video)
      cmd = ["python",
        	"./crop-video.py",
        	"--inp", inp,
        	"--dm", "256"]
      cmd1 = ["python",
             "./crop-video.py",
             "--inp", inp,
             "--dm", "1024"]
      subprocess.Popen(cmd).wait()
      subprocess.Popen(cmd1).wait()


      res_256 = os.path.join(name_folder, 'result256.mkv')
      print(res_256)
      output_folder = os.path.join(name_folder, 'first_frame.png')
      '''
      Step 2: Extract the first frame from the cropped videos
      '''
      cmd = ["ffmpeg",
             "-i", res_256,
             "-vframes", "1",
             "-q:v", "1",
             output_folder]
      subprocess.Popen(cmd).wait()

      '''
      Step 3: Run demo of first order model with all the input images (frame) and the cropped videos
      '''
      res = os.path.join(name_folder, 'result.mp4')
      cmd = ["python",
             "./demo.py",
             "--config", "config/vox-256.yaml",
             "--driving_video", res_256,
             "--source_image", output_folder,
             "--checkpoint", "checkpoints/vox-cpk.pth.tar",
             "--relative",
             "--adapt_scale",
             "--result_video", res]
      subprocess.Popen(cmd).wait()

      '''
      Step 4: now that we have the output of FOM, we need to divide into frames the 1024 video and the 256 output video.
      To do so, we need to check what is the frame rate
      '''
      if not os.path.exists(res):
          sys.stderr.write("ERROR: filename %r was not found!" % (res,))
      out = subprocess.check_output(
          ["ffprobe", res, "-v", "0", "-select_streams", "v", "-print_format", "flat", "-show_entries",
           "stream=r_frame_rate"])
      rate = out.decode("utf-8").split('"')[1].split('/')
      if len(rate) == 1:
          fps = float(rate[0])
      if len(rate) == 2:
          fps = float(rate[0]) / float(rate[1])

      frames_folder = os.path.join(name_folder, 'frames_LR')
      framescommand = 'fps=' + str(fps)
      try:
          os.mkdir(frames_folder)
      except OSError:
          print("Creation of the directory %s failed" % frames_folder)
      cmd = ["ffmpeg",
             "-i", res,
             "-q:v", "1",
             "-vf", framescommand,
             frames_folder + '/' + "res1%04d.png"]
      print(cmd)
      subprocess.Popen(cmd).wait()


      res_1024 = os.path.join(name_folder, 'result1024.mkv')
      frames_folder = os.path.join(name_folder, 'frames_HR')
      try:
          os.mkdir(frames_folder)
      except OSError:
          print("Creation of the directory %s failed" % frames_folder)

      cmd = ["ffmpeg",
             "-i", res_1024,
             "-q:v", "1",
             "-vf", framescommand,
             frames_folder + '/' + "res1%04d.png"]
      print(cmd)
      subprocess.Popen(cmd).wait()
