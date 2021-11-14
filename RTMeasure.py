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
scale = 3
wP = 210*scale
hP = 297*scale


########## end Settings ############

while(1):
    if webcam: success, img = cap.read()
    else: img = cv2.imread(path)

    img, cts = utils.getConts(img, draw=True)
    if len(cts) !=0 :
        biggest = cts[0][2]
        print(biggest)
        #imgWarp = utils.imgWarp(img, biggest, wP, hP)
        #cv2.imshow("warped", imgWarp)
        
    img = cv2.resize(img, (0,0), None, 0.5, 0.5)
    
        
    cv2.imshow('Orig', img)
    cv2.waitKey(1)
