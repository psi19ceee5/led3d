#!/usr/bin/env python3

import sqlite3
import sys
import math
import board
import neopixel
import time
sys.path.append('..')
import src.config as cfg
import src.dbio as db
import src.led as led

class led(led.proto_led) :
    def __init__(self, id, ledchain, pos=(0, 0, 0), col=(0, 0, 0)) :
        super().__init__(id, pos=pos, col=col)
        self.ledchain = ledchain
        
    def commit(self) :
        id = self.led_id
        r = round(255*self.r)
        g = round(255*self.g)
        b = round(255*self.b)
        
        self.ledchain.pixels[id] = (r, g, b)
                
class ledchain :
    def __init__(self, brightness=0.2, ORDER=neopixel.RGB) :
        
        # Choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D18
        # NeoPixels must be connected to D10, D12, D18 or D21 to work.
        pixel_pin = board.D18

        # The number of NeoPixels
        num_pixels = cfg.NLEDs
        
        # The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
        # For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
        ORDER = neopixel.RGB
        
        self.pixels = neopixel.NeoPixel(
            pixel_pin, num_pixels, brightness=brightness, auto_write=False, pixel_order=ORDER
        )
                
    def commit(self) :
        self.pixels.show()

if __name__ == "__main__" :
    
    conn = db.create_connection("../db/calibinfo.sqlite")

    chain = ledchain()
    leds = []
    for id in range(cfg.NLEDs) :
        try :
            (x, y, z) = db.read_led(conn, id)
            leds.append(led(id, chain, (x, y, z), (1, 1, 1)))
        except Exception :
            print("[ERROR]: LED", id, " not in database.")
    
    fps = 10.
    phase_r = 0
    phase_g = 60*math.pi/180.
    phase_b = 120*math.pi/180.
    t0 = time.time()
    dt = 0
    while True :
        t = time.time() - t0
        for led in leds :
            r = math.sin(0.5*math.pi*t - (math.pi/0.25)*led.z + phase_r)**2
            g = math.sin(0.5*math.pi*t - (math.pi/0.25)*led.z + phase_g)**2
            b = math.sin(0.5*math.pi*t - (math.pi/0.25)*led.z + phase_b)**2
            led.set_rgb(r, g, b)
            led.commit()
        chain.commit()
        dt = time.time() - t0 - t
        time.sleep(1./fps - dt if dt < 1./fps else 0)
