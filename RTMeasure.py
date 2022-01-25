'''
@file RTMeasure.py
@description This file uses simple object detection and tracking to measure the real-time distance of two objects, determined
        by two mouse clicks, the tip and the reflection in that order. The object tracking uses a simple class written by
        Sergio Canu
        for a tutorial and a file utils.py

    Instructions for use:
        The top half of the file contains settings for the thresholds of the background subtraction and the history length
        As well as the minimum area (in pixels) of objects and the binary threshold value to include for object detection.
        Additionally, the reference distance value is set by default to 5 (assuming the tip can be adjusted exactly 5 microns)
        Finally, the users can change their start and end keys for calibrating the pixels per distance value.
        display_bounding_rects can be set by the user to true if they want to see the bounding rectangles for the tip and
        the reflection.

        To use:
            Start by clicking on the tip to display it, followed by the reflection of the tip.
            Once both are detected, press b to store the x,y value for the tip at the beginning of calibration.
            Move the tip 5 microns and then press f to finish calibrating.

            If at all there is a mistake or an error in the display, press r to restart.

            Press q when ready to quit the program. 
    
'''
import cv2
from tracker import *
import utils as ut

''' ====== USER SETTINGS ====='''
## Settings for object detection 
vThresh = 40 # for background subtraction
hist = 100
minArea = 200 # for ut.obj_detector
minThresh = 254 # for ut.obj_detector
REF_DIST = 5
display_bounding_rects = True

# change for user preference 
startKey = ord("b") #begin calibration
endKey = ord("f") # end calibration

''' END SETTINGS '''



# Create tracker object with Sergio's Helper Class
tracker = EuclideanDistTracker()
# capture object
cap = cv2.VideoCapture(0)

# Pixel calibration initial values 
startX = None 
startY= None
endX = None
endY = None

#list of click points 
xPt = []
yPt = []
tip = None #integer ID  
refl = None #integer ID

##Sets the points where the user clicks 
def click_point(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        xPt.append(x)
        yPt.append(y)

# Object detection from Stable camera
object_detector = cv2.createBackgroundSubtractorMOG2(history=hist, varThreshold=vThresh)
ut.print_instructions()
''' =============== End Setup ============ '''

## RT Loop 
while True:
    ret, frame = cap.read()
    if not ret:
        break
    #Tie clicks to the frame 
    cv2.namedWindow('Frame')
    cv2.setMouseCallback('Frame', click_point)
    
    key = cv2.waitKey(30) # 30 ms between frames 

    # Detecting objects
    mask, detections = ut.obj_detector(frame, minArea, minThresh)

    #Object Tracking
    boxes_ids = tracker.update(detections)

    
    for box_id in boxes_ids:    # Checks every tracked object - could be optimized but the loop is very fast anyway
        x, y, w, h, id = box_id
            
        # Set the object ID of the tip
        if len(xPt):
            if xPt[0] >= x and xPt[0] <= x+w and yPt[0] >= y and yPt[0] <= y + h:
                if tip is None:
                    tip = id
                    xPt = []
                    yPt = []
                elif refl is None:
                    refl = id  
        # Only cares about tip
        if tip is not None :
            if id == tip:
                px = int((x + x + h)/2)
                py = (y + h) # lowest point on
                if display_bounding_rects: 
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    cv2.putText(frame, "Tip", (x, y - 15), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
        # Only cares about reflection
        if refl is not None:
            if id == refl:
                zpX = x # leftmost point
                zpY = y # highest point on reflection
                if display_bounding_rects: 
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                    cv2.putText(frame, "Reflection", (x, y - 15), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2) 

                    ## Calibrating the pixels for 5 microns
            if key == startKey:
                startX = px
                startY = py
                print("Press 'f' once tip has moved 5 microns to finish calibration.")
                startDone = True
            if key== endKey:
                endX = px
                endY = py
                print("Calibrated.")
                endDone=True
                
            # calculates the distance    
            D = ut.distance((zpX,zpY),(px, py))
            '''uncomment if want the vertical distance only'''
            #D = ut.distance((px,zpY),(px, py))

            #Calculate and display distances
            if startY is not None and endY is not None:
                px_per_dist = abs(endY - startY) / REF_DIST #microns
                distance = " {:.1f} microns".format(D / px_per_dist)
                cv2.line(frame, (5, py), (10, zpY),(0, 0, 255), 2)
                cv2.putText(frame, distance, (10, 300), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
            else:
                cv2.putText(frame, "Press 'b' then 'f'", (10, 40), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
                cv2.putText(frame, "to calibrate", (10, 65), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
                
    cv2.imshow("Frame", frame)
    
    ## reset the initial values if 'r' is pressed
    if key == ord("r"):
        xPt = []
        yPt = []
        tip = None
        refl = None
        startX = None
        startY = None
        endX = None
        endY = None
        px_per_dist = None 

    # Press 'q' to quit
    if key == ord("q"): #s on keyboard
        break
# release the recording
cap.release()
cv2.destroyAllWindows()
