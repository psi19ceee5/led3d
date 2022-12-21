#!/usr/bin/env python3

import cv2 as cv
import numpy as np
import math
import argparse
import src.utilities as ut

coords = []

def mouseclick(event, y, x, flags, params) :
    if event == cv.EVENT_LBUTTONDOWN:
        print("Pixel clicked:", (x,y))
        ut.draw_reticle(image, (x,y))
        cv.imshow('ImgCapture', image)
        coords.append((x,y))

if __name__ == "__main__" :
    
    parser = argparse.ArgumentParser(description='Script for calibrating pixel distance to real-world distance')
    parser.add_argument('-c', metavar='CAM', type=int, required=False, help='override default camera port 0')
    args = parser.parse_args()
    
    cam = 0
    if args.c :
        cam = args.c


    cam = cv.VideoCapture(cam)
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
    
    factor = dist/pxdist
    file = open("/tmp/lengthcalib", "w")
    file.write(str(factor))
    file.close()
    print("Conversion factor [meter / pixel]:", factor)
    print("Press any key to quit")
    cv.waitKey(0)