'''
@author Clay Boyd
@brief This file is a utilities package for RTMeasure.py
        It contains helper functions for object detection, distance calculation, midpoint calculation,
        average calculation, and then a print function for the instructions.
'''
import cv2
from scipy.spatial import distance as dist
import numpy as np

def obj_detector(frame, minArea = 1000, minThresh = 254):
    '''
        uses binary threshold detection to separate the background and objects
        then uses simple chain approximation to store the contours or edges of the objects,
        @param frame - the image frame to analyze
        @param minArea - the minumum area (in pixels) to consider a detection
        @param minThresh - the minimum light value of the foreground objects

        @return mask - the new frame
        @return detections - a list of [x,y, width, height] of all of the objects detected
    '''
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, mask = cv2.threshold(frame, minThresh, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    detections = []
    for cnt in contours:
        # Filter detections that are too small
        area = cv2.contourArea(cnt)
        if area > minArea:
            x, y, w, h = cv2.boundingRect(cnt)
            detections.append([x, y, w, h])

    return mask, detections

def distance(a, b):
    '''
        Returns the distance in pixels
        @param a (tuple) - the first point
        @param b (tuple) the second point
        @return d (float) the distance between a and b
    '''
    d = dist.euclidean((a[0], a[1]), (b[0], b[1]))
    return d


def midpoint (a, b):
    '''
        Returns the midway point
        @param a (tuple) - the first point
        @param b (tuple) the second point
        @return the midpoint of a and b
    '''
    return (0.5*(a[0]+b[0]), 0.5*(a[1]+b[1]))

def avg (n1, n2):
    '''
        @param n1 (float or int) the first value
        @param n2 (float or int) the second value 
        @return the integer value of the average between two numbers
    '''
    return int(0.5*(n1 + n2))

def print_instructions():
    '''
        prints the instructions for user in terminal
    '''
    
    instr = """Instructions: \n
            1) Click the tip. \n
            2) Click on the reflection of the tip \n
            3) Press 'b' when you are ready to begin
            calibrating the distance per pixels.\n\n
            Press 'r' to reset values if there is a calibration or click error."""
    print(instr)
                


    
