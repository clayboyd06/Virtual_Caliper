import cv2
from tracker import *
import utils2 as ut

# Create tracker object
tracker = EuclideanDistTracker()
# capture object
cap = cv2.VideoCapture(0)

# Object detection from Stable camera
object_detector = cv2.createBackgroundSubtractorMOG2(history=100, varThreshold=40)

## Play with for camera settings
y1 = 340
y2 = 720
x1 = 500
x2 = 800
minArea = 1000
zeroPoint = 700

# change for user preference 
startKey = ord('b') #begin calibration
endKey = ord('f') # end calibration
while True:
    ret, frame = cap.read()
    height, width, _ = frame.shape

    if not ret:
        break
    key = cv2.waitKey(30)
    # Filter Region of interest -> need to change for camera Settings
    roi = frame[y1: y2,x1: x2]

    mask, detections = ut.obj_detector(roi, minArea)


    # 2. Object Tracking
    boxes_ids = tracker.update(detections)
    startY= 0
    endY = 0
    for box_id in boxes_ids:
        x, y, w, h, id = box_id
        D = ut.dist((((x + x + w) // 2),y),(((x + x + w) // 2), zeroPoint))
        if key == startKey:
            startY = y
        if key== endKey:
            endY = y
        px_per_dist = (endY - startY) / 5 #microns
        if px_per_dist == 0:
            distance = " {:.1f} pixels".format(D)
        else:
            distance = " {:.1f} um".format(D / px_per_dist)
        cv2.putText(roi, distance, (x, y - 15), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
        cv2.rectangle(roi, (x, y), (x + w, y + h), (0, 255, 0), 3)

    cv2.imshow("Region of Interest", roi)
    cv2.imshow("Frame", frame)
    cv2.imshow("Mask", mask)

   
    if key == 27: #s on keyboard
        break

cap.release()
cv2.destroyAllWindows()
