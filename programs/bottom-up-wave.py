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
    def commit(self) :
        id = self.led_id
        r = round(255*self.r)
        g = round(255*self.g)
        b = round(255*self.b)
        print(r, g, b)
        
        # Choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D18
        # NeoPixels must be connected to D10, D12, D18 or D21 to work.
        pixel_pin = board.D18

        # The number of NeoPixels
        num_pixels = cfg.NLEDs
        
        # The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
        # For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
        ORDER = neopixel.RGB
        
        pixels = neopixel.NeoPixel(
            pixel_pin, num_pixels, brightness=0.2, auto_write=False, pixel_order=ORDER
        )
        
        pixels[id] = (r, g, b)
        pixels.show()
        
        

if __name__ == "__main__" :
    
    conn = db.create_connection("../db/calibinfo.sqlite")

    leds = []
    for id in range(cfg.NLEDs) :
        try :
            (x, y, z) = db.read_led(conn, id)
            leds.append(led(id, (x, y, z), (1, 1, 1)))
        except Exception :
            print("[ERROR]: LED", id, " not in database.")
    
    fps = 25
    phase_r = 0
    phase_g = 60*math.pi/180.
    phase_b = 120*math.pi/180.
    t0 = time.time()
    while True :
        t = time.time() - t0
        for led in leds :
            r = math.sin(0.5*math.pi*t - (math.pi/0.25)*led.z + phase_r)**2
            g = math.sin(0.5*math.pi*t - (math.pi/0.25)*led.z + phase_g)**2
            b = math.sin(0.5*math.pi*t - (math.pi/0.25)*led.z + phase_b)**2
            led.set_rgb(r, g, b)
            led.commit()
