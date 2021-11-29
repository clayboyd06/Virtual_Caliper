import cv2
import numpy as np
import os
import argparse
import utils

###### Setup #######
webcam = False

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=False,
	help="path to the input image")
ap.add_argument("-w", "--ref_width", type=float, required=False,
	help="width of the reference object in the image (in cm)")
args = vars(ap.parse_args())

path = "test_img/two.png" ##args ["image"]

cap = cv2.VideoCapture(0)
cap.set(10, 160)
cap.set(3, 1920)
cap.set(4, 1080)

pixel_scale = 3 #TODO = D / ref_width = 5 microns - establish D with a calibration frame as numb pixels.
                ## Get top bottom and

if webcam: success, img = cap.read()
else: img = cv2.imread(path)

img = utils.img_detection(img)
