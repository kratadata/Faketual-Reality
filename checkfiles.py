import matplotlib

matplotlib.use('Agg')
import os
from skimage import io

path = '/media/apaccagne/hdd1/vox/test'

subdirs = [x[0] for x in os.walk(path)]
for subdir, directories, files in os.walk(path):
    #print(subdir)
    for file in files:
        #print(file)
        try:
            # print(path)
            #print(subdir + '/' + file)
            img = io.imread(subdir + '/' + file)
        except (IOError, SyntaxError, ValueError) as e:
            print('Bad file:', subdir + '/' + file)




    '''print (subdir)
    files = os.listdir(subdir)   #questi dovrebbero essere i file dentro, quindi i video mp4
    #print(files)

    num_frames = len(files)
    #print(num_frames)

    for element in files:
        print(element)
        try:
            #print(path)
            print(subdir + '/' + element)
            img = io.imread(subdir + '/' + element)
        except (IOError, SyntaxError) as e:
            print('Bad file:', os.path.join(path, element))'''


