from scipy.spatial import distance as dist
import os
from imutils import perspective
from imutils import contours
import numpy as np
import argparse
import imutils
import cv2



ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=False,
	help="path to the input image")
ap.add_argument("-w", "--ref_width", type=float, required=False,
	help="width of the reference object in the image (in cm)")
args = vars(ap.parse_args())

webcam = True
cap = cv2.VideoCapture(0)
cap.set(10, 160)
cap.set(3, 1920)
cap.set(4, 1080)

def midpoint (a, b):
    return (0.5*(a[0]+b[0]), 0.5*(a[1]+b[1]))

def measure_image(image, ref_width=1):
    # load the image, convert it to grayscale, and blur it slightly
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (3, 3), 0)


    # perform edge detection, then perform a dilation + erosion to
    # close gaps in between object edges
    edged = cv2.Canny(gray, 150, 300)
    edged = cv2.dilate(edged, None, iterations=1)
    edged = cv2.erode(edged, None, iterations=1)
    # find contours in the edge map
    cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    # sort the contours from left-to-right and, then initialize the
    # distance colors and reference object
    (cnts, _) = contours.sort_contours(cnts)
    colors = ((0, 0, 255), (240, 0, 159), (0, 165, 255), (255, 255, 0),
            (255, 0, 255))
    refObj = None

    # loop over the contours individually
    for c in range(4):
            # if the contour is not sufficiently large, ignore it
            if cv2.contourArea(cnts[c]) < 100:
                    continue
            # compute the rotated bounding box of the contour
            boxN = cv2.minAreaRect(cnts[c])
            boxN = cv2.cv.BoxPoints(boxN) if imutils.is_cv2() else cv2.boxPoints(boxN)
            boxN = np.array(boxN, dtype="int")
            boxN = perspective.order_points(boxN)
            # compute the center of the bounding box
            cXN = np.average(boxN[:, 0])
            cYN = np.average(boxN[:, 1])
            
            if c != 0 and c!= 1:
                boxO = cv2.minAreaRect(cnts[c-1])
                boxO = cv2.cv.BoxPoints(boxO) if imutils.is_cv2() else cv2.boxPoints(boxO)
                boxO = np.array(boxO, dtype="int")
                boxO = perspective.order_points(boxO)
                cXO = np.average(boxO[:, 0])
                cYO = np.average(boxO[:, 1])
    # if this is the first contour we are examining (i.e.,
            # the left-most contour), we presume this is the
            # reference object
            ## TODO: Make it universal in that the reference object does not have to be the first object. 
            if refObj is None:
                    # unpack the ordered bounding box, then compute the
                    # midpoint between the top-left and top-right points,
                    # followed by the midpoint between the top-right and
                    # bottom-right
                    (tl, tr, br, bl) = boxN
                    (tlblX, tlblY) = midpoint(tl, bl)
                    (trbrX, trbrY) = midpoint(tr, br)
                    # compute the Euclidean distance between the midpoints,
                    # then construct the reference object
                    D = dist.euclidean((tlblX, tlblY), (trbrX, trbrY))
                    refObj = (boxN, (cXN, cYN), D / ref_width) #D / ref width is pixels per cm
                    continue
            # draw the contours on the image
            #orig = image.copy()
            #cv2.drawContours(orig, [boxN.astype("int")], -1, (0, 255, 0), 2)
            #cv2.drawContours(orig, [boxO.astype("int")], -1, (0, 255, 0), 2)
            #cv2.drawContours(orig, [refObj[0].astype("int")], -1, (0, 255, 0), 2)
            # distance from ref coords
            if c > 1:
                #refCoords = np.vstack([boxO])
                refCoords = np.vstack([(midpoint(boxO[0], boxO[1])),(midpoint(boxO[2], boxO[3]))])
            #objCoords = np.vstack([boxN])
            objCoords = np.vstack([(midpoint(boxN[0], boxN[1])),(midpoint(boxN[2], boxN[3]))])
            
    # loop over the original points
            if c > 1 :
                #for ((xA, yA), (xB, yB), color) in zip(refCoords, objCoords, colors):
                newimg = image.copy()
                color = colors[1]
                # draw circles corresponding to the current points and
                # connect them with a line
                cv2.circle(newimg, (int(refCoords[0][0]), int(refCoords[0][1])), 5, color, -1)
                cv2.circle(newimg, (int(objCoords[0][0]), int(objCoords[0][1])), 5, color, -1)
                cv2.line(newimg, (int(refCoords[0][0]), int(refCoords[0][1])), (int(objCoords[0][0]), int(objCoords[0][1])),
                        color, 2)
                # compute the Euclidean distance between the coordinates,
                # and then convert the distance in pixels to distance in
                # units
                D = dist.euclidean((refCoords[0][0], refCoords[0][1]), (objCoords[0][0], objCoords[0][1])) / refObj[2]
                (mX, mY) = midpoint((refCoords[0][1], refCoords[0][1]), (objCoords[0][0], objCoords[0][1]))
                cv2.putText(newimg, " {:.1f} cm".format(D), (int(mX), int(mY - 10)),
                cv2.FONT_HERSHEY_SIMPLEX, 0.55, color, 2)
                # show the output image
                cv2.imshow("Image", newimg)
                cv2.waitKey(0)
                

while(1):
    if not webcam: image = image = cv2.imread(args["image"])
    else: image = success, image = cap.read()
    measure_image(image) 
    


