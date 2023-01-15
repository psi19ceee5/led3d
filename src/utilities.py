#!/usr/bin/env python3

import math
import numpy as np

deg2rad = math.pi/180.
rad2deg = 180./math.pi

def info(*txt):
    print("\033[30;102;1m[INFO]:\033[0m", *txt)
    
def warn(*txt) :
    print("\033[30;103;1m[WARNING]:\033[0m", *txt)

def error(*txt) :
    print("\033[30;101;1m[ERROR]:\033[0m", *txt)

def draw_reticle(image, imax) :
    ix = imax[1]
    iy = imax[0]
    off = 5
    
    if len(np.shape(image)) == 3 :
        for px in range(15) :
            for th in range(-1,1) :
                if(iy-off-px > 0 and ix+th < len(image[0])) :
                    image[iy-off-px,ix+th,:] = 255
                if(iy+off+px < len(image) and ix+th < len(image[0])) :
                    image[iy+off+px,ix+th,:] = 255
                if(iy+th < len(image) and ix-off-px > 0) :
                    image[iy+th,ix-off-px,:] = 255
                if(iy+th < len(image) and ix+off+px < len(image[0])) :
                    image[iy+th,ix+off+px,:] = 255
    elif len(np.shape(image)) == 2 :
        for px in range(15) :
            for th in range(-1,1) :
                if(iy-off-px > 0 and ix+th < len(image[0])) :
                    image[iy-off-px,ix+th] = 255
                if(iy+off+px < len(image) and ix+th < len(image[0])) :
                    image[iy+off+px,ix+th] = 255
                if(iy+th < len(image) and ix-off-px > 0) :
                    image[iy+th,ix-off-px] = 255
                if(iy+th < len(image) and ix+off+px < len(image[0])) :
                    image[iy+th,ix+off+px] = 255
    else :
        error("shape of image doesn't match. No reticle can be drawn.")