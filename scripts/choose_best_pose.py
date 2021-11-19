'''
Aim: find the best matching between the first frame of the driving video, and several others images.
How to use the script:
python choose_best_pose.py path_of_the_video path_of_image_folder path_of_predictor_file
'''

# import the necessary packages
from scipy.spatial import distance as dist
from imutils import face_utils
import numpy as np
import argparse
import imutils
import time
import dlib
import os
import cv2
import matplotlib.pyplot as plt
import subprocess
import getopt, sys
import logging

""" 
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger()
logger.addHandler(logging.FileHandler('test.log', 'a'))
print = logger.info 
"""

#compute aspect ratio of the eye
def eye_aspect_ratio(eye):
    # compute the euclidean distances between the two sets of
    # vertical eye landmarks (x, y)-coordinates
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])
    # compute the euclidean distance between the horizontal
    # eye landmark (x, y)-coordinates
    C = dist.euclidean(eye[0], eye[3])
    # compute the eye aspect ratio
    ear = (A + B) / (2.0 * C)
    # return the eye aspect ratio
    return ear, (A + B)/2 , C

#compute euclidean distance between the lip up and the lip down (https://www.hackster.io/raspimage/face-parts-recogntion-055f10 following the order of landmarks there)
def mouth_aspect_ratio(mouth):
    horizontal_dist = dist.euclidean(mouth[12], mouth[16])
    return dist.euclidean(mouth[14], mouth[18]), horizontal_dist

def rect_to_bb(rect):
    # take a bounding predicted by dlib and convert it
    # to the format (x, y, w, h) as we would normally do
    # with OpenCV
    x = rect.left()
    y = rect.top()
    w = rect.right() - x
    h = rect.bottom() - y
    # return a tuple of (x, y, w, h)
    return (x, y, w, h)

def euclidean_distance_landmarks(a, b):
    return np.linalg.norm(a-b)

#compute the distance and sum a penality given by eyes and mouth specific distances
def compute_value(driving, height_mouth, horizontal_mouth, ear, eye_vertical_L, eye_vertical_R, eye_horizontal_L, eye_horizontal_R, distance):
    mouth_horizontal_difference = abs(height_mouth - driving.height_mouth)
    mouth_vertical_difference = abs(horizontal_mouth - driving.horizontal_mouth)
    eye_aspect_ratio = abs(ear - driving.ear)
    eye_horizontal_difference = abs(eye_horizontal_L - driving.eye_horizontal_L) + abs(eye_horizontal_R - driving.eye_horizontal_R)
    eye_vertical_difference = abs(eye_vertical_L - driving.eye_vertical_L) + abs(eye_vertical_R - driving.eye_vertical_R)

    return distance + mouth_horizontal_difference + mouth_vertical_difference + eye_horizontal_difference + eye_vertical_difference

def choose_best_pose(path_driving, path_images, path_predictor):
    '''
    :param path_driving: is the full path o the driving video
    :param path_images: path_images is a folder where all the input images are
    :return: the best image choice
    '''
    # initialize dlib's face detector (HOG-based) and then create
    # the facial landmark predictor
    shape_predictor = path_predictor
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(shape_predictor)

    # grab 2 frames, resize
    # them, and convert them to grayscale
    # channels)
    if(os.path.isfile(os.path.splitext(path_driving)[0] + 'output_image.png')):
        driving = frame_driving(os.path.splitext(path_driving)[0] + 'output_image.png', detector, predictor)
    else:
        cmd = ["ffmpeg", "-i", path_driving, "-vf", "select=eq(n\,0)", "-q:v", "100", os.path.splitext(path_driving)[0] ]
        subprocess.Popen(cmd).wait()
        driving = frame_driving(os.path.splitext(path_driving)[0] + 'output_image.png', detector, predictor) 
    
    min_value = 99999999
    frame_list = os.listdir(path_images)

    for path_img_i in sorted(frame_list):
        if path_img_i.endswith('.png'):
            frame_2 = cv2.imread(os.path.join(path_images, path_img_i ))
            frame_2 = imutils.resize(frame_2, width=512)
            gray_2 = cv2.cvtColor(frame_2, cv2.COLOR_BGR2GRAY)
            rects_2 = detector(gray_2, 0)

            for rect_2 in rects_2:
                shape = predictor(gray_2, rect_2)
                shape = face_utils.shape_to_np(shape)

                (x, y, w, h) = face_utils.rect_to_bb(rect_2)
                cropped_frame_2 = frame_2[y:y + h, x:x + w]
                cropped_frame_2 = cv2.resize(cropped_frame_2, (512, 512))
                rect_2 = dlib.rectangle(0, 0, 512, 512)

                plt.figure()
                # plt.imshow(cropped_frame_2)
                gray_cropped_2 = cv2.cvtColor(cropped_frame_2, cv2.COLOR_BGR2GRAY)
                shape = predictor(gray_cropped_2, rect_2)
                shape_2_cropped = face_utils.shape_to_np(shape)

                leftEye = shape_2_cropped[lStart:lEnd]
                rightEye = shape_2_cropped[rStart:rEnd]
                mouth = shape_2_cropped[mStart:mEnd]
                leftEAR, eye_vertical_L, eye_horizontal_L = eye_aspect_ratio(leftEye)
                rightEAR, eye_vertical_R, eye_horizontal_R = eye_aspect_ratio(rightEye)
                height_mouth, horizontal_mouth = mouth_aspect_ratio(mouth)

                # average the eye aspect ratio together for both eyes
                ear = (leftEAR + rightEAR) / 2.0

                # compute the convex hull for the left and right eye, then
                # visualize each of the eyes
                leftEyeHull = cv2.convexHull(leftEye)
                rightEyeHull = cv2.convexHull(rightEye)

                cv2.drawContours(cropped_frame_2, [leftEyeHull], -1, (0, 255, 0), 1)
                cv2.drawContours(cropped_frame_2, [rightEyeHull], -1, (0, 255, 0), 1)

                # plt.figure()
                # plt.imshow(cropped_frame_2)

                distance = euclidean_distance_landmarks(driving.shape_1_cropped, shape_2_cropped)
                value = compute_value(driving, height_mouth, horizontal_mouth, ear, eye_vertical_L, eye_vertical_R,
                                    eye_horizontal_L, eye_horizontal_R, distance)
                print(path_img_i)
                if (value < min_value):
                    min_value = value
                    best = path_img_i
                print('distance value at the end is: ', value)
                if height_mouth > MOUTH_TRESH:
                    print('mouth is open')
                    if horizontal_mouth > 140:
                        print('mouth is smiling')
                    else:
                        print('mouth is not smiling')
                elif height_mouth <= MOUTH_TRESH and height_mouth > CLOSED_MOUTH_TRESH:
                    print('mouth is half closed')
                    if horizontal_mouth > 140:
                        print('mouth is smiling')
                    else:
                        print('mouth is not smiling')
                else:
                    print('mouth is closed')
                if ear >= EYE_AR_THRESH and ear <= 0.30:
                    print('half open eyes')
                elif ear > 0.30:
                    print('open eyes')
                elif ear < EYE_AR_THRESH:
                    print('closed eyes')

    os.rename(path_images +"/" + best, path_images + "/" + 'best_pose.png') 


class frame_driving():
    def __init__(self, path, detector, predictor):
        frame = cv2.imread(path)
        frame = imutils.resize(frame, width=412)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # detect faces in the grayscale frame 1
        rects = detector(gray, 0)
        for rect in rects:
            # determine the facial landmarks for the face region, then
            # convert the facial landmark (x, y)-coordinates to a NumPy
            # array
            shape = predictor(gray, rect)
            shape = face_utils.shape_to_np(shape)
            # convert dlib's rectangle to a OpenCV-style bounding box
            # [i.e., (x, y, w, h)], then draw the face bounding box
            (x, y, w, h) = face_utils.rect_to_bb(rect)
            rect = dlib.rectangle(0, 0, w, h)
            cropped_frame = frame[y:y + h, x:x + w]
            cropped_frame = cv2.resize(cropped_frame, (512, 512))
            rect = dlib.rectangle(0, 0, 512, 512)

            # plt.figure()
            # plt.imshow(cropped_frame)
            gray_cropped = cv2.cvtColor(cropped_frame, cv2.COLOR_BGR2GRAY)

            # I repeat the landmarks extraction because now I have the cropped image
            shape = predictor(gray_cropped, rect)
            self.shape_1_cropped = face_utils.shape_to_np(shape)

            # extract the left and right eye coordinates, then use the
            # coordinates to compute the eye aspect ratio for both eyes
            leftEye = self.shape_1_cropped[lStart:lEnd]
            rightEye = self.shape_1_cropped[rStart:rEnd]
            mouth = self.shape_1_cropped[mStart:mEnd]
            self.leftEAR, self.eye_vertical_L, self.eye_horizontal_L = eye_aspect_ratio(leftEye)
            self.rightEAR, self.eye_vertical_R, self.eye_horizontal_R = eye_aspect_ratio(rightEye)
            self.height_mouth, self.horizontal_mouth = mouth_aspect_ratio(mouth)
            # average the eye aspect ratio together for both eyes
            self.ear = (self.leftEAR + self.rightEAR) / 2.0
            # compute the convex hull for the left and right eye, then
            # visualize each of the eyes
            leftEyeHull = cv2.convexHull(leftEye)
            rightEyeHull = cv2.convexHull(rightEye)

            # draw in the image
            cv2.drawContours(cropped_frame, [leftEyeHull], -1, (0, 255, 0), 1)
            cv2.drawContours(cropped_frame, [rightEyeHull], -1, (0, 255, 0), 1)

            # value swe are interested in for classification are height_mouth, horizontal_mouth ear
            # self.classify_values()

            self.cropped_frame = cropped_frame
            # plt.figure()
            # plt.imshow(cropped_frame)

    def classify_values(self):
        # ok now we can classify
        if self.height_mouth > MOUTH_TRESH:
            print('mouth is open')
            if self.horizontal_mouth > 140:
                print('mouth is smiling')
            else:
                print('mouth is not smiling')
        elif self.height_mouth <= MOUTH_TRESH and self.height_mouth > CLOSED_MOUTH_TRESH:
            print('mouth is half_closed')
            if self.horizontal_mouth > 140:
                print('mouth is smiling')
            else:
                print('mouth is not smiling')
        else:
            print('mouth is closed')
        if self.ear >= EYE_AR_THRESH and self.ear <= 0.30:
            print('half open eyes')
        elif self.ear > 0.30:
            print('open eyes')
        elif self.ear < EYE_AR_THRESH:
            print('closed eyes')




# grab the indexes of the facial landmarks for the left and
# right eye, respectively
(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]
(jStart, jEnd) = face_utils.FACIAL_LANDMARKS_IDXS["jaw"]
(mStart, mEnd) = face_utils.FACIAL_LANDMARKS_IDXS["mouth"]

# define two constants, tresholds to classify whether the eye is open or closed and same for the mouth (https://www.pyimagesearch.com/2017/04/24/eye-blink-detection-opencv-python-dlib/ eye blink)
EYE_AR_THRESH = 0.05
MOUTH_TRESH = 15
CLOSED_MOUTH_TRESH = 5

# Get full command-line arguments
full_cmd_arguments = sys.argv

# Keep all but the first
argument_list = full_cmd_arguments[1:]
print(argument_list)
choose_best_pose(argument_list[0], argument_list[1], argument_list[2])