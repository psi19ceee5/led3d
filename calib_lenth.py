#!/usr/bin/env python3

import cv2 as cv
import numpy as np
import math
import utilities as ut

coords = []

def mouseclick(event, y, x, flags, params) :
    if event == cv.EVENT_LBUTTONDOWN:
        print("Pixel clicked:", (x,y))
        ut.draw_reticle(image, (x,y))
        cv.imshow('ImgCapture', image)
        coords.append((x,y))

if __name__ == "__main__" :

    cam = cv.VideoCapture(0)
    result, image = cam.read()

    if not result :
        print("[ERROR]: No image has been taken. Perhaps, try another camera port.")
        exit
    else :
        print("Shape of image: ", np.shape(image))
    
    print("Click on two pixels in the image. Make sure that the pixels point approximately to the same plane orthogonal to the camera axis.")
    cv.imshow('ImgCapture', image)
    cv.setMouseCallback('ImgCapture', mouseclick)
    
    while len(coords) < 2 :
        cv.waitKey(10)
        
    dist = float(input("Enter the separation (in meter) of the two pixels in the real world: "))
    pxdist = math.sqrt((coords[0][0] - coords[1][0])**2 + (coords[0][1] - coords[1][1])**2)
    
    print("Conversion factor [meter / pixel]:", dist/pxdist)    
    print("Press any key to quit")
    cv.waitKey(0)