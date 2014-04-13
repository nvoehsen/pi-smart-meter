import cv2
import sys
import numpy as np
from datetime import datetime, date, time

# 75 Umdrehungen sind 1 kWh
# 1/75 kWh in Ws =>(Wolfram Alpha) 48000 Ws

wattSecPerU = 48000.0
cropFromY = 90
cropToY   = 200
lower_red = np.array([0,180,50])
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

def readFrame():
    result, fullframe = vidFile.read();
    retframe = fullframe[cropFromY:cropToY,:] if result else fullframe 
    return result, retframe

    
def frame_something(f):
    framecpy = f.copy()
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
        
def frame_writeout(f, mask):
    res  = cv2.bitwise_and(f,f, mask= 255 - mask)
    dat = datetime.now() 
    cv2.imwrite("frame-%s.jpg" %dat, res)      
 
    #    cv2.imshow("frameWindow", res)
    #cv2.waitKey(int(1/fps *1000)) # time to wait between frames, in mSec

class ModelState:
    def __init__(self):
        self.currentlyred = 0
        self.conseczeros  = 0
        self.changed = 0
        
    def update(self, i):
        self.updatezeros(i)
        self.updatered(i)
    def updatezeros(self, i):
        if i<1:
            self.conseczeros += 1
        else:
            self.conseczeros=0
    def updatered(self, i):
        if self.currentlyred == 0 and i > 10 :
            self.currentlyred = 1
            self.changed = 1
        elif self.currentlyred == 1 and self.conseczeros > 2 : 
            self.currentlyred = 0
            self.changed = -1
        else:
            self.changed = 0
        

            

        
# fileonly nFrames = int(vidFile.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT)) 
   # one good way of namespacing legacy openCV: cv2.cv.*
# fileonly print "frame number: %s" %nFrames
#    fps = vidFile.get(cv2.cv.CV_CAP_PROP_FPS)
#    print "FPS value: %s" %fps
framenum=0

lasttime = datetime.now()
ret, frame = readFrame() 

disc = ModelState()

print disc.currentlyred

while ret:  

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Rot ist bei [0,0,255] 
    # Grau / farblos ist auf der Achse [ i, i, i]
    # Die Roete wird definiert durch die Projektion auf die Achse i,i,i
    # Die Projektion ist entlang von [ -1, -1, 2 ] 
    # Skalarprodukt damit positiv => rot

    mask = cv2.inRange(hsv, lower_red, upper_red)
 
    #frame_writeout(frame, mask)

    mheight, mwidth = mask.shape
 
    framenum += 1 
    perc = mask.sum() / mheight / mwidth
    print framenum, "; ", perc


    currtime = datetime.now()
    disc.update(perc)
    
    if disc.changed == -1  :
        delta = currtime - lasttime
        watts =  wattSecPerU / delta.total_seconds()
        print currtime, "; ", watts
        lasttime = currtime 


    ret, frame = readFrame() # read next frame, get next return code


