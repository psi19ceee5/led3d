#!/usr/bin/env python3

import cv2 as cv
import numpy as np
import utilities as ut

if __name__ == "__main__" :

    cam = cv.VideoCapture(0)
    result, image = cam.read()
    
    if not result :
        print("[ERROR]: No image has been taken. Perhaps, try another camera port.")
        exit
    else :
        print("Shape of image: ", np.shape(image))
        
    # note: colors in BGR
    filtered_img = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    
    imax = np.unravel_index(filtered_img.argmax(), np.shape(filtered_img))
    print("Brightest pixel (first occurence):", imax)
    print("Brightness:", filtered_img[imax])
    
    hot_pixels = 0
    for i_ in range(len(filtered_img)) :
        for j_ in range(len(filtered_img[i_])) :
            if filtered_img[i_][j_] == filtered_img[imax] :
                ut.draw_reticle(image, (i_, j_))
                hot_pixels += 1
                
    print("Hottest pixels:", hot_pixels)
    
    cv.imshow("ImgCapture", image)
    cv.waitKey(0)
    cv.destroyAllWindows()
    #cv.imwrite("ImgCapture.png", image)
    