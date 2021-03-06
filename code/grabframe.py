import cv2
import sys
import numpy as np
from datetime import datetime, date, time

# Usage grabframe.py [VIDFILENAME]
# VIDFILENAME: optional video file name
# creates two jpgs in current dir

# The red mark is recognized by a color between these values
lower_red = np.array([0,160,50])
upper_red = np.array([60,255,255])


try:
    if len(sys.argv) < 2 :
        vidFile = cv2.VideoCapture(0)
    else :
        vidFile = cv2.VideoCapture(sys.argv[1])
except:
    print "problem opening input stream"
    sys.exit(1)
if not vidFile.isOpened():
    print "capture stream not open"
    sys.exit(1)

#capture image
result, frame = vidFile.read();

#write to disk
dat = datetime.now().strftime("%Y%m%d%H%M%S") 
cv2.imwrite("frame-orig-%s.jpg" %dat, frame)      

#transform to hsv
hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

#select all red pixels in mask
mask = cv2.inRange(hsv, lower_red, upper_red)

#mix the mask into the image to make the mask visible
res  = cv2.bitwise_and(frame, frame, mask= 255 - mask)

cv2.imwrite("frame-mask-%s.jpg" %dat, res)      


