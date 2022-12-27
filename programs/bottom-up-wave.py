#!/usr/bin/env python3

import sys
import math
import time
sys.path.append('..')
import src.config as cfg
import src.dbio as db
import src.led as led

if __name__ == "__main__" :
    
    conn = db.create_connection("../db/calibinfo.sqlite")

    chain = led.ledchain()
    leds = []
    for id in range(cfg.NLEDs) :
        try :
            (x, y, z) = db.read_led(conn, id)
            leds.append(led.led(id, chain, (x, y, z), (1, 1, 1)))
        except Exception as e :
            print("[ERROR]:", e, "( LED", id,")")
    
    fps = 10.
    phase_r = 0
    phase_g = 60*math.pi/180.
    phase_b = 120*math.pi/180.
    t0 = time.time()
    dt = 0
    while True :
        t = time.time() - t0
        for LED in leds :
            r = math.sin(0.5*math.pi*t - (math.pi/0.75)*LED.z + phase_r)**2
            g = math.sin(0.5*math.pi*t - (math.pi/0.75)*LED.z + phase_g)**2
            b = math.sin(0.5*math.pi*t - (math.pi/0.75)*LED.z + phase_b)**2
            LED.set_rgb(r, g, b)
            LED.commit()
        chain.commit()
        dt = time.time() - t0 - t
        time.sleep(1./fps - dt if dt < 1./fps else 0)
