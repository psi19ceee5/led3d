#!/usr/bin/env python3

import sys
import board
import neopixel

num_pixels = 150

pixels = neopixel.NeoPixel(board.D18, num_pixels)

try:
    ledid = int(sys.argv[1])
except TypeError:
    print("Please enter an integer value between 0 and ", num_pixels-1, "!")
    sys.exit(1)
except IndexError:
    print("Please specify the ID of the LED you want to turn on (between 0 and ", num_pixels -1, ")!")
    sys.exit(1)

if ledid < num_pixels and 0 <= ledid:
    pixels[ledid] = (0, 0, 255)
    pixels.show()
else:
    print("The LED ID needs to be between 0 and ", num_pixels-1, "!")
