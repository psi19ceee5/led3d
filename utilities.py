#!/usr/bin/env python3

import math

deg2rad = math.pi/180.
rad2deg = 180./math.pi


def draw_reticle(image, imax) :
    ix = imax[1]
    iy = imax[0]
    off = 5
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
