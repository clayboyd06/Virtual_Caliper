import cv2
import numpy as np

def getConts(img, cThr = [100,150], showCanny=False, minArea=1000, filter =0, draw=False):
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (5,5), 1)
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
            print("here!")
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.02*peri, True)
            bbox = cv2.boundingRect(approx)

            if (filter > 0):
                if len(approx) == filter:
                    finalContours.append((len(approx), area, approx, bbox, c))
                    print("boop")
            else:
                finalContours.append((len(approx), area, approx, bbox, c))
                print("blipp")

    finalContours = sorted(finalContours, key = lambda x:x[1] , reverse = True)

    if draw:
        for con in finalContours:
            cv2.drawContours(img, con[4], -1, (0,0,255), 3)

    return img, finalContours

## reorders points to follow the order:
## TL, BL, TR, BR
def reorder(points):
    newPoints = np.zeros_like(points)
    points = points.reshape((4,2))
    
    add = points.sum(1)
    diff = np.diff(points, axis=1)
    
    newPoints[0] = points[np.argmin(add)]
    points[3] = points[np.argmax(add)]
    newPoints[1] = points[np.argmin(diff)]
    newPoints[2] = points[np.argmax(diff)]
    return newPoints

def imgWarp(img, points, w, h, pad=20):
    #points = reorder(points)
    pts1 = np.float32(points)
    pts2 = np.float32([[0,0],[w,0],[0,h],[w,h]])
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    imgWarp = cv2.warpPerspective(img, matrix, (w,h))
    imgWarp = imgWarp[pad:imgWarp.shape[0]-pad, pad:imgWarp.shape[1]-pad]
    return imgWarp
