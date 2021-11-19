'''
This script is needed to generate several animations for images and videos in specific folders 
'''

import os
import subprocess

rootdir = '/local/home/apaccagne/Desktop/facesfom'

for root, dirs, files in os.walk(rootdir):
    print("root = ", root)
    print("dirs = ", dirs)
    print("files = ", files)
    for file in files:
        res = '/local/home/apaccagne/Desktop/results/8_alearrabbiata'
        folder = (os.path.join(rootdir, file))
        res = os.path.join(res, file)
        res = res.replace('png', 'mp4')
        #print(folder, res)

        cmd = ["python",
        	"./demo.py",
        	"--config", "config/vox-256.yaml",
        	"--driving_video", "/project/PycharmProjects/first-order-model/trials_outputs/alepose.mp4",
        	"--source_image", folder,
            "--checkpoint", "checkpoints/vox-cpk.pth.tar",
        	"--relative",
            "--adapt_scale",
            "--result_video", res]
        #print(cmd)
        subprocess.Popen(cmd).wait()
