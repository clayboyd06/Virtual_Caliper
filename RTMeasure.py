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




########## end Settings ############

while(1):
    if webcam: success, img = cap.read()
    else: img = cv2.imread(path)

    img, cts = utils.getConts(img, draw=True)

    if len(cts) !=0 :
        biggest = cts[0][2]
        top, bottom = utils.top_bottom(img, cts)
        
        D = utils.distance(top, bottom)
        mx, my = utils.midpoint(top, bottom)
        # if(calibrate):px_per_dist = D
        #if px_per_dist is not none: distance = D / px_per_dist
        #print("Top: {} Bottom: {} Distance: {} ".format(top, bottom, D / pixel_scale))

        #Show distance on monitor
        cv2.circle(img, (int(top[0]), int(top[1])), 5, (0, 0, 255), -1)
        cv2.circle(img, (int(bottom[0]), int(bottom[1])), 5, (0, 0, 255), -1)
        cv2.line(img, (int(top[0]), int(top[1])), (int(bottom[0]), int(bottom[1])), (0, 0, 255), 2)
        cv2.putText(img, " {:.1f} um".format(D), (int(my), int(my - 10)),
                cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 0, 255), 2)
        
    img = cv2.resize(img, (0,0), None, 0.5, 0.5)
    
        
    cv2.imshow('Frame', img)
    cv2.waitKey(1)
