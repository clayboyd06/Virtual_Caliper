import cv2
from scipy.spatial import distance as dist
import numpy as np

## TODO play with threshhold settings to get best canny for the printer tips
def getConts(img, cThr = [100,150], showCanny=False, minArea=1000, filter =0, draw=False):
    '''
    getConts uses canny edge detection to get the contours of an image.

    input parameters:
        img the cv2 frame
        cThr - the threshold values for canny. Defaults are [100, 150]
        showCanny - will open a window to show the canny edge detection. False by default
        minArea - the minium area of an object to be returned. Default is 1000
        filter - filters the number of points on an object edge. 0 by default
        draw - boolean to control if the bounding box is drawn on the frame - False by default
    
    returns the image data and an array called finalContours which contains the data of the size
    of a contour, the area, the approximation of the points, the bounding box, the min and max points, and
    the raw data.
    '''
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (5,5), 1)
    #thresh = cv2.threshold(imgBlur, 220, 255, cv2.THRESH_BINARY_INV)[1]
    edges = cv2.Canny(imgBlur, cThr[0], cThr[1])
    kernal = np.ones((5,5))
    dilated = cv2.dilate(edges, kernal, iterations=3)
    imgThresh = cv2.erode(dilated, kernal, iterations=2)
    if showCanny: cv2.imshow('Contour', imgThresh)

    cnts, hier = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    finalContours = []
    for c in cnts:
        area = cv2.contourArea(c)
        if area > minArea:
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.02*peri, True)
            bbox = cv2.boundingRect(approx)
            miny = tuple(c[c[:, :, 1].argmax()][0])
            maxy = tuple(c[c[:, :, 1].argmin()][0])
            #print(miny, maxy)
        
            if (filter > 0):
                if len(approx) == filter:
                    finalContours.append((len(approx), area, approx, bbox, miny, maxy, c))
            else:
                finalContours.append((len(approx), area, approx, bbox, miny, maxy, c))

    finalContours = sorted(finalContours, key = lambda x:x[1] , reverse = True)

    if draw:
        for con in finalContours:
            cv2.drawContours(img, con[6], -1, (0,0,255), 3)

    return img, finalContours

## TODO debug - getting working with semi- RTOS
## TODO decide how to use image detection to measure between objects :
    ## ie boolean enable or direct measure 
def img_detection(ref, img, frame = None):
    '''
    uses SIFT technique to recognize object in image
    Input paremeters:
        ref - reference image to detect object from
        img - the image to locate the object in
        frame - a frame mask to cut off a region of the input frame
    '''
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ref = cv2.cvtColor(ref, cv2.COLOR_BGR2GRAY)
    
    sift = cv2. xfeatures2d.SIFT_create()
    ref_kp, ref_desc = sift.detectAndCompute(ref, None)
    keypoints_2, descriptors_2 = sift.detectAndCompute(imgGray,None)

    bf = cv2.BFMatcher(cv2.NORM_L1, crossCheck=True)
    matches = bf.match(ref_desc,descriptors_2)
    matches = sorted(matches, key = lambda x:x.distance)
   
    imgMatches = cv2.drawMatches(ref, ref_kp, img, keypoints_2, matches[:50], img, flags=2)
    return imgMatches #maybe it only has to return a boolean to enable measurement


def frame(img, x1, x2, y1, y2):
    '''
    returns a frame within the specified region
    '''
    cropped = img[x1:x2, y1:y2]
    return cropped

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

## TODO make more efficient... maybe the object detection can handle this 
def top_bottom(img, conts):
    '''
        returns the (x,y) coordinates of the top point of the bottom object
        and the bottom point of the top object
    '''
    maxy = 0
    miny = np.inf
    top = 0
    bottom =0
    for i in range(len(conts)):
        if conts[i][4][1] < miny:
            miny = conts[i][4][1]
            bottom = conts[i][4]
        if conts[i][5][1] > maxy:
            maxy = conts[i][5][1]
            top = conts[i][5]
    return top, bottom
    



