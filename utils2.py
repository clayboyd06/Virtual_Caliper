import cv2
from scipy.spatial import distance as dist
import numpy as np

def obj_detector(frame, minArea = 1000):
    mask = object_detector.apply(frame)
    _, mask = cv2.threshold(mask, 254, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    detections = []
    for cnt in contours:
        # Calculate area and remove small elements
        area = cv2.contourArea(cnt)
        if area > minArea:
            #cv2.drawContours(roi, [cnt], -1, (0, 255, 0), 2)
            x, y, w, h = cv2.boundingRect(cnt)
            detections.append([x, y, w, h])

    return mask, detections

def distance(a, b):
    '''
        Returns the distance in pixels
    '''
    return dist.euclidean((a[0], a[1]), (b[0], b[1]))


def midpoint (a, b):
    '''
        Returns the midway point 
    '''
    return (0.5*(a[0]+b[0]), 0.5*(a[1]+b[1]))
