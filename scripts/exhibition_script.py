'''
This script is choosing randomly a video from a folder of many of them, then calls the network to
synthesized the output video.
Inside the path specified in 'image' there is the desired image.
Inside the path specified in 'videos' there are three different driving videos.
The name of the output file is the same as the one of the input image, and it can be put in the desired path indicated
by 'output_path'
'''

import os
import subprocess
import random
import cv2
import sys


#file path (change)
#image = ''
#driving video folder path (change)
#driving_video = ''
#output saving path (change)


#result = os.path.join(output_path, image_name + '.mp4')
#result = ''

def pad(i):
    if(len(i) == 1):
        return('00' + str(i))
    elif(len(i) == 2):
        return('0' + str(i))
    else: #3 cifre
        return(str(i))

'''
Run the network
'''
def runDeepfake(driving_video, image, result):
                
        output_path = result[:-14]
        image_name = os.path.split(image)[1]
        image_name = os.path.splitext(image_name)[0] #name of the image without extension

        cmd = ["python",
                "./demo.py",
                "--config", "config/vox-512.yaml",
                "--driving_video", driving_video,
                "--source_image", image,
                "--checkpoint", "checkpoints/checkpoint.pth.tar",
                "--relative",
                "--adapt_scale",
                "--result_video", result]

        subprocess.Popen(cmd).wait()


        '''
        Now the video is saved in the folder chosen.
        I will divide it into frames first. Then enhance the frames, and finally re-putting them together. 
        '''
        cap = cv2.VideoCapture(result)

        frames_folder = os.path.join(output_path, 'frames_512')
        try:
                if not os.path.exists(frames_folder):
                        os.makedirs(frames_folder)
        except OSError:
                print('Error: Creating directory of data %s ', frames_folder)


        totalframes = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        currentFrame = 0
        #check the fps
        out = subprocess.check_output(["ffprobe", result, "-v", "0", "-select_streams", "v", "-print_format", "flat", "-show_entries","stream=r_frame_rate"])
        rate = out.decode("utf-8").split('"')[1].split('/')
        if len(rate) == 1:
                fps = float(rate[0])
        if len(rate) == 2:
                fps = float(rate[0]) / float(rate[1])
        image_name = os.path.basename(os.path.normpath(image)).replace('.png', '')

        folder = os.path.join(output_path, 'frames_512', image_name)
        name = os.path.join(folder, pad(str(currentFrame)) + '.png')
        try:
                if not os.path.exists(folder):
                        os.makedirs(folder)
        except OSError:
                print('Already existing folder %s ', folder)
        
        while (currentFrame < totalframes):
                # Capture frame-by-frame
                ret, frame = cap.read()

                name = os.path.join(folder, pad(str(currentFrame)) + '.png')
                cv2.imwrite(name, frame)
                currentFrame += 1


# Get full command-line arguments
full_cmd_arguments = sys.argv

# Keep all but the first
argument_list = full_cmd_arguments[1:]
print(argument_list)
runDeepfake(argument_list[0], argument_list[1], argument_list[2])