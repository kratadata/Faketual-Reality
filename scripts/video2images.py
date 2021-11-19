import os
import subprocess

input_video = '/home/paulina/Desktop/visitors/visitor.webm'
output_path = '/home/paulina/Desktop/visitors/'

cmd = ["ffmpeg", "-i", input_video, "-vsync", "vfr", "-q:v", "5", output_path + "img_%03d.png"]
subprocess.Popen(cmd).wait()
