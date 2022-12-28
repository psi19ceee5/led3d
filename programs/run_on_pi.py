#!/usr/bin/env python3

import sys
import time
sys.path.append('..')
import src.config as cfg
import src.dbio as db
import src.led as led
from os.path import exists
from os import remove

# specify program here
#import programs.bottom_up_wave as prg
import programs.left_right_right_left as prg

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
    tref = t0
    dt = 0
    while True :
        t = time.time() - t0
        program.set_state(t)
        if time.time() - tref > 10 :
            if exists("/tmp/LEDSTOP") :
                remove("/tmp/LEDSTOP")
                chain.off()
                chain.commit()
                break
            else :
                tref = time.time()
        for LED in leds :
            program.set_coordinates(LED.led_id, LED.x, LED.y, LED.z, t)
            r, g, b = program.get_rgb()
            LED.set_rgb(r, g, b)
            LED.commit()
        chain.commit()
        dt = time.time() - t0 - t
        time.sleep(1./fps - dt if dt < 1./fps else 0)
