import cv2
import sys
import numpy as np
from datetime import datetime, date, time

# 75 Umdrehungen sind 1 kWh
# 1/75 kWh in Ws =>(Wolfram Alpha) 48000 Ws

wattSecPerU = 48000

try:
    #fileonly vidFile = cv2.VideoCapture(sys.argv[1])
    vidFile = cv2.VideoCapture(0)
except:
    print "problem opening input stream"
    sys.exit(1)
if not vidFile.isOpened():
    print "capture stream not open"
    sys.exit(1)

# fileonly nFrames = int(vidFile.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT)) 
   # one good way of namespacing legacy openCV: cv2.cv.*
# fileonly print "frame number: %s" %nFrames
#    fps = vidFile.get(cv2.cv.CV_CAP_PROP_FPS)
#    print "FPS value: %s" %fps
framenum=0
currentlyred=0
lasttime = datetime.now()
ret, frame = vidFile.read() # read first frame, and the return code of the function.
while ret:  
# note that we don't have to use frame number here, we could read from a live written file.
#    print "yes"
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    framecpy = frame.copy()
    px = frame[100,100]
    #    print px
    lightgray= [200,200,200]
    #print "hsv: ", hsv[100,130]
    framecpy[115:125,95:105] = lightgray
    # waagerecht: 80, 200
    framecpy[80,] =  lightgray
    framecpy[200,] = lightgray
    # senkrecht: 100, 200
    framecpy[:,100] = lightgray
    framecpy[:,200] = lightgray

    # Rot ist bei [0,0,255] 
    # Grau / farblos ist auf der Achse [ i, i, i]
    # Die Roete wird definiert durch die Projektion auf die Achse i,i,i
    # Die Projektion ist entlang von [ -1, -1, 2 ] 
    # Skalarprodukt damit positiv => rot

    lower_red = np.array([0,180,50])
    upper_red = np.array([60,255,255])

    mask = cv2.inRange(hsv, lower_red, upper_red)
 
    mheight, mwidth = mask.shape
 
    framenum += 1 
    perc = mask.sum() / mheight / mwidth
    print framenum, "; ", perc


    currtime = datetime.now()
    if currentlyred == 0 and perc > 5 :
        currentlyred = 1
    elif currentlyred == 1 and perc < 1 : 
        currentlyred = 0
        delta = currtime - lasttime
        watts =  wattSecPerU / delta.seconds
        print currtime, "; ", watts
        lasttime = currtime 
        
             
#    res  = cv2.bitwise_and(frame,frame, mask= mask)      
#    cv2.imshow("frameWindow", res)
#    cv2.waitKey(int(1/fps *1000)) # time to wait between frames, in mSec
    ret, frame = vidFile.read() # read next frame, get next return code


