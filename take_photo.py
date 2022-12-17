#!/usr/bin/env python3

import cv2 as cv
import numpy as np

def draw_reticle(image, imax) :
    ix = imax[1]
    iy = imax[0]
    off = 5
    for px in range(15) :
        for th in range(-1,1) :
            image[iy-off-px,ix+th,:] = 255
            image[iy+off+px,ix+th,:] = 255
            image[iy+th,ix-off-px,:] = 255
            image[iy+th,ix+off+px,:] = 255

cam = cv.VideoCapture(2)
result, image = cam.read()

if not result :
    print("[ERROR]: No image has been taken. Perhaps, try another camera port.")
    exit
else :
    print("Shape of image: ", np.shape(image))
    
# note: colors in BGR
filtered_img = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

print(filtered_img)

imax = np.unravel_index(filtered_img.argmax(), np.shape(filtered_img))
print(imax)

draw_reticle(image, imax)

cv.imshow("ImgCapture", filtered_img)
cv.waitKey(0)
cv.destroyAllWindows()
#cv.imwrite("ImgCapture.png", image)
    