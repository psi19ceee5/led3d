#!/usr/bin/env python3

import sys
import time
sys.path.append('..')
import src.config as cfg
import src.dbio as db
import src.led as led

# specify program here
import programs.bottom_up_wave as prg

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

    program = prg.program()
    t0 = time.time()
    dt = 0
    while True :
        t = time.time() - t0
        for LED in leds :
            program.set_coordinates(LED.x, LED.y, LED.z, t)
            r, g, b = program.fkt()
            LED.set_rgb(r, g, b)
            LED.commit()
        chain.commit()
        dt = time.time() - t0 - t
        time.sleep(1./fps - dt if dt < 1./fps else 0)
