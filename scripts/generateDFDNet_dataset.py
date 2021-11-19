'''
Script needed to generate the synthesized videos for 512x512 version of the tecoGAN dataset.
Inside the folder facesfom there are three different folders containing images with similar poses, and a driving video.
The folder facesfom is in the path /cluster/work/infk_mtc/alessiapacca/facesfom
Then we also divide all the videos into frames.
After this, we will call the script scriptino.py of DFDNet that will enhance the images. 
'''
import os
import subprocess

import sys

rootdir = '/local/home/apaccagne/Desktop/facesfom'
#in this path we should put all the folders with
#faces

i = 0
for root, dirs, files in os.walk(rootdir):
    #print("root = ", root) #one of the root for faces folders
    #print("dirs = ", dirs) #no dirs
    #print("files = ", files) #all the faces
    head_tail = os.path.split(root)
    #if(head_tail[1] == 'sorridente'):
    if(head_tail[1] != 'video' and head_tail[1] != 'results' and head_tail[1] != 'leggermenteaperta'):
        for file in files: #every single image inside the specific folder
            '''            
            Step 1: Generate synthesized video
            '''
            res = os.path.join(root, 'video', os.listdir(os.path.join(root, 'video'))[0]) #driving video
            element = (os.path.join(root, file)) #la immagine
            print(element)
            namefile = file.replace('png', 'mp4')
            namefile = namefile.replace('jpg', 'mp4')
            result = os.path.join(root, 'results', 'res' + namefile)
            print(result)
            head_tail2 = os.path.split(result)
            print(head_tail2[1])

            cmd = ["python",
                "./demo.py",
                "--config", "config/vox-512.yaml",
                "--driving_video", res,
                "--source_image", element,
                "--checkpoint", "checkpoints/checkpoint.pth.tar",
                "--relative",
                "--adapt_scale",
                "--result_video", result]
            #print(cmd)
            subprocess.Popen(cmd).wait()



            '''
            Step 2: divide in frames with the correct frame rate
            '''
            if not os.path.exists(result):
                sys.stderr.write("ERROR: filename %r was not found!" % (result,))
            out = subprocess.check_output(
                ["ffprobe", result, "-v", "0", "-select_streams", "v", "-print_format", "flat", "-show_entries",
                 "stream=r_frame_rate"])
            rate = out.decode("utf-8").split('"')[1].split('/')
            if len(rate) == 1:
                fps = float(rate[0])
            if len(rate) == 2:
                fps = float(rate[0]) / float(rate[1])
    
    
            frames_folder = os.path.join('/cluster/work/infk_mtc/alessiapacca/framesfacesfom', str(i))
            i = i+1
            framescommand = 'fps=' + str(fps)
            try:
                os.mkdir(frames_folder)
            except OSError:
                print("Creation of the directory %s failed" % frames_folder)
            cmd = ["ffmpeg",
                   "-i", result,
                   "-q:v", "1",
                   "-vf", framescommand,
                   frames_folder + '/' + "res1%04d.png"]
            subprocess.Popen(cmd).wait()
