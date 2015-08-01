import cv2
import sys
import numpy as np
from datetime import datetime, date, time

# Usage processvid_pi.py DIR [VIDFILENAME]
# DIR: directory to contain data files
# VIDFILENAME: optional video file name

# constant declaration
# 75 revolutions are 1 kWh
# 1/75 kWh in Ws =>(Wolfram Alpha) 48000 Ws

wattSecPerU = 48000.0

# The crop values are needed, otherwise processing takes much too long on PI
# These are extracted by hand from a sample frame grab
cropFromY = 170
cropToY   = 250
# The red mark is recognized by a color between these values
lower_red = np.array([0,160,50])
upper_red = np.array([60,255,255])

dir = sys.argv[1]
print "Directory: {}".format(dir)


try:
    if len(sys.argv) < 3 :
        vidFile = cv2.VideoCapture(0)
    else :
        vidFile = cv2.VideoCapture(sys.argv[2])
except:
    print "problem opening input stream"
    sys.exit(1)
if not vidFile.isOpened():
    print "capture stream not open"
    sys.exit(1)

def getFileName():
    dtime = datetime.now()
    return dir + "/" + dtime.strftime("%Y-%m-%d_%H%M%S") + "_capture.csv"
    
def openFile():
    filename = getFileName()
    return open(filename, 'a')

#get cropped frame from video device    
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

#dump frame and mask to file            
def frame_writeout(f, mask):
    res  = cv2.bitwise_and(f,f, mask= 255 - mask)
    dat = datetime.now() 
    cv2.imwrite("frame-%s.jpg" %dat, res)      
 
    #    cv2.imshow("frameWindow", res)
    #cv2.waitKey(int(1/fps *1000)) # time to wait between frames, in mSec


# To improve the detection of the red mark passing through, the past state of the mark detection is used
# An instance of this class holds information about previously detected disk states
# currentlyred: Is the mark currently visible
# conseczeros:  How many frames with no mark were there previously
# changed:      Has the mark status changed? 1: mark appeared 0: no change -1: mark disappeared

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

#print disc.currentlyred

outfile = openFile()

while ret:  

    #transform to hsv
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    #select all red pixels in mask
    mask = cv2.inRange(hsv, lower_red, upper_red)

    # calculate perc, i.e. the mean of the mask pixels
    mheight, mwidth = mask.shape
    perc = mask.sum() / mheight / mwidth

    # update disc state with perc
    disc.update(perc)

    # for debugging uncomment, writes all capture files to disk
    #    frame_writeout(frame, mask)

    #default outputs
    timestring = ""
    wattstring = ""

    framenum += 1 
    currtime = datetime.now()
        
    #detected red:
    if disc.changed == -1  :
        #daily logroll
        if currtime.day != lasttime.day :
            outfile.close();
            outfile = openFile();
        #calc current watts using time since last passage of the mark 
        delta = currtime - lasttime
        watts =  wattSecPerU / delta.total_seconds()
        #reset timestamp
        lasttime = currtime
        #set strings for output
        timestring = str(currtime)
        wattstring = repr(watts)
    
    outfile.write( "{0};{1};{2};{3}\n".format( str(framenum),                                               repr(perc), timestring, wattstring) )

    ret, frame = readFrame() # read next frame, get next return code


