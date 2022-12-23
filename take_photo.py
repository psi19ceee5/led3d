#!/usr/bin/env python3

import cv2 as cv
import numpy as np
import argparse
import src.utilities as ut

if __name__ == "__main__" :
    
    parser = argparse.ArgumentParser(description='Takes a photograph with the webcam and identifies the brightest pixel(s). An angle can be specified for 3d reconstruction')
    parser.add_argument('-a', metavar='ANGLE', type=float, required=False, help='specify the angle by which the system has been rotated with respect to the camera axis')
    parser.add_argument('-c', metavar='CAM', type=int, required=False, help='override default camera port 0')
    parser.add_argument('-d', action='store_true', help='run in debug mode: image is shown with reticles on brightest pixels and more information is printed to screen')
    parser.add_argument('-n', metavar='NUMPIC', type=int, required=False, help='a running number may be specified for the picture taken. If specified, an output image is written to /tmp')
    args = parser.parse_args()
    
    angle = 0.
    cam = 0
    debug = False
    npic = -1
    if args.a is not None :
        angle = args.a
    if args.c is not None :
        cam = args.c
    if args.d :
        debug = True
    if args.n >= 0 :
        npic = args.n

    cam = cv.VideoCapture(cam)
    result, image = cam.read()
    
    if not result :
        print("[ERROR]: No image has been taken. Perhaps, try another camera port.")
        exit
    else :
        if debug :
            print("Shape of image: ", np.shape(image))
        
    # note: colors in BGR
    #filtered_img = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    filtered_img = np.copy(image[:,:,2])
    filtered_img_cpy = np.copy(filtered_img)
    
    imax = np.unravel_index(filtered_img.argmax(), np.shape(filtered_img))
    if debug :
        print("Brightest pixel (first occurence):", imax)
        print("Brightness:", filtered_img[imax])
    
    hot_pixels = 0
    for i_ in range(len(filtered_img)) :
        for j_ in range(len(filtered_img[i_])) :
            if filtered_img[i_][j_] == filtered_img[imax] :
                ut.draw_reticle(image, (i_, j_))
                ut.draw_reticle(filtered_img_cpy, (i_, j_))
                hot_pixels += 1
                
    if debug :
        print("Hottest pixels:", hot_pixels)
        print("Viewing angle:", angle, "deg")
        cv.imshow("ImgCapture", image)
        cv.waitKey(0)
        cv.destroyAllWindows()
    
    if not debug :
#        print(npic, angle, imax[1], imax[0], filtered_img[imax]) # remove last variable
        print(npic, angle, imax[1], imax[0])
        if npic >= 0 :
            cv.imwrite("/tmp/ImgCapture-"+str(npic)+".png", filtered_img_cpy)
