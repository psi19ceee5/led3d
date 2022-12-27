#!/usr/bin/env python3

import sys
import math
sys.path.append('..')
import src.config as cfg
import src.dbio as db
import src.sim_led as led

if __name__ == "__main__" :
    
    conn = db.create_connection("/home/philip/Projects/led3d/db/calibinfo.sqlite")

    chain = led.sim_ledchain()
    leds = []
    for id in range(cfg.NLEDs) :
        try :
            (x, y, z) = db.read_led(conn, id)
            leds.append(led.sim_led(id, chain, (x, y, z), (1, 1, 1)))
        except Exception :
            print("[ERROR]: LED", id, " not in database.")
    
    fps = 10
    phase_r = 0
    phase_g = 60*math.pi/180.
    phase_b = 120*math.pi/180.
    for frame in range(250) :
        t = frame/fps
        for LED in leds :
            r = math.sin(0.5*math.pi*t - (math.pi/0.75)*LED.z + phase_r)**2
            g = math.sin(0.5*math.pi*t - (math.pi/0.75)*LED.z + phase_g)**2
            b = math.sin(0.5*math.pi*t - (math.pi/0.75)*LED.z + phase_b)**2
            LED.frame = frame
            LED.set_rgb(r, g, b)
            LED.commit()
        chain.commit()
