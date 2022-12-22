#!/usr/bin/env python3

import board
import neopixel

pixels = neopixel.NeoPixel(board.D18, 150)

pixels.fill((0, 0, 0))
