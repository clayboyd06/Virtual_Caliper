import cv2
from tracker import *
import utils as ut
import argparse


# Create tracker object with Sergio's Helper Class
tracker = EuclideanDistTracker()
# capture object
cap = cv2.VideoCapture(0)
#cap.set(10, 160)
#cap.set(3, 1920)
#cap.set(4, 1080)
#print(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
#print(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

startY= None
endY = None

# Object detection from Stable camera
object_detector = cv2.createBackgroundSubtractorMOG2(history=100, varThreshold=40)


#video source:
webcam = True
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=False,
	help="path to the input image")
args = vars(ap.parse_args())
path = "test_img/two.png" ##args ["image"]

## Play with for camera settings
y1 = 0
y2 = 720
x1 = 400
x2 = 810
minArea = 100
zeroPoint = 650 #pixel position of reflection of tip, or estimate of the surface if known

# change for user preference 
startKey = ord("b") #begin calibration
endKey = ord("f") # end calibration


''' =============== End Settings ============ '''

while True:
    if webcam: ret, frame = cap.read()
    else: img = cv2.imread(path)
    height, width, _ = frame.shape

    if not ret:
        break
    key = cv2.waitKey(30)
    # Filter Region of interest -> need to change for camera Settings
    roi = frame[y1: y2,x1: x2]

    mask, detections = ut.obj_detector(roi, minArea)


    # 2. Object Tracking and Distance Computing
    boxes_ids = tracker.update(detections)

    for box_id in boxes_ids: # if cam stable - should only be 1 or 2 box_ids
        x, y, w, h, id = box_id
        D = ut.distance((((x + x + w) // 2),zeroPoint),(((x + x + w) // 2), y))
        if key == startKey:
            startY = y
            print("Press f once tip has moved 5 microns to calibrate")
        if key== endKey:
            endY = y
            print("Calibrated")
        if startY is not None and endY is not None:
            px_per_dist = (endY - startY) / 5 #microns
            distance = " {:.1f} um".format(D / px_per_dist)
            cv2.line(roi, (int(x+w/2), y), (int(x+w/2), zeroPoint),(0, 0, 255), 2)
            cv2.putText(roi, distance, (x, ut.avg(y, zeroPoint)), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
        else:
            distance = " {:.1f} pixels".format(D)
            cv2.putText(roi, distance, (x, y - 15), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
        cv2.rectangle(roi, (x, y), (x + w, y + h), (0, 255, 0), 3)

    # 3 display the measurement 
    #cv2.imshow("Region of Interest", roi)
    #cv2.imshow("Mask", mask)
    cv2.imshow("Frame", frame)
    

   
    if key == ord("q"): #s on keyboard
        break

cap.release()
cv2.destroyAllWindows()
