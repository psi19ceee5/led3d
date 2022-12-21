#!/usr/bin/env python3

import sys
import board
import neopixel

pixels = neopixel.NeoPixel(board.D18, 150)

ledid = sys.argv[1]

pixels[ledid] = (0, 0, 255)
