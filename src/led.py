#!/usr/bin/env python3
import sys
sys.path.append('..')
import src.config as cfg
import src.proto_led as pled
import board
import neopixel
    
class ledchain(pled.proto_ledchain) :
    def __init__(self, brightness=0.2, ORDER=neopixel.RGB) :
        
        # Choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D18
        # NeoPixels must be connected to D10, D12, D18 or D21 to work.
        pixel_pin = board.D18

        num_pixels = cfg.NLEDs
        
        # For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
        ORDER = neopixel.RGB
        
        self.pixels = neopixel.NeoPixel(
            pixel_pin, num_pixels, brightness=brightness, auto_write=False, pixel_order=ORDER
        )
        
    def commit(self) :
        self.pixels.show()
                
class led(pled.proto_led) :
    def __init__(self, id, ledchain, pos=(0, 0, 0), col=(0, 0, 0)) :
        super().__init__(id, ledchain, pos=pos, col=col)
        
    def commit(self) :
        id = self.led_id
        r = round(255*self.r)
        g = round(255*self.g)
        b = round(255*self.b)
        
        self.ledchain.pixels[id] = (r, g, b)
