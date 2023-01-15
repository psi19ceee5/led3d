#!/usr/bin/env python3

import board
import neopixel
import sys
sys.path.append('..')
import src.config
import src.utilities as ut

num_pixels = src.config.NLEDs

pixels = neopixel.NeoPixel(board.D18, num_pixels)

try:
    ledid = int(sys.argv[1])
except (TypeError, ValueError):
    ut.error("please enter an integer value between 0 and ", num_pixels-1, "!")
    sys.exit(1)
except IndexError:
    ut.error("please specify the ID of the LED you want to turn on (between 0 and ", num_pixels -1, ")!")
    sys.exit(1)

if ledid < num_pixels and 0 <= ledid:
    pixels[ledid] = (0, 0, 255)
    pixels.show()
else:
    ut.error("the LED ID needs to be between 0 and ", num_pixels-1, "!")
    sys.exit(1)
