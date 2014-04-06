#!/usr/bin/python
# -*- coding: utf-8 -*-

import cv2

#image = cv.LoadImage("jeverjungs.jpg")
cam = cv2.VideoCapture(0)
s,image=cam.read()
if s:
    cv2.namedWindow("Camera", 1)
    cv2.imshow("Camera", image)
    c = cv2.waitKey(0)
    cv2.destroyWindow("Camera")

