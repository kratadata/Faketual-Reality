import os
import PIL
from PIL import Image

#file path (change)
images = '/home/paulina/Desktop/visitors/test'
#output saving path (change)
output_path = '/home/paulina/Desktop/visitors/test'

for element in os.listdir(images):
        image = PIL.Image.open(os.path.join(images, element))
        width, height = image.size
        print(width, height)
        print(element)
        smaller = min(width, height)
        if(width < height):
            center = height/2
            upperbound = center + width/2
            lowerbound = center - width/2
            box = (0, lowerbound, width, upperbound)
            crop = image.crop(box)
            crop.save(os.path.join(output_path, element))
        elif(width > height):
            center = width / 2
            upperbound = center + height / 2
            lowerbound = center - height / 2
            box = (lowerbound, 0, upperbound, height)
            crop = image.crop(box)
            crop.save(os.path.join(output_path, element))