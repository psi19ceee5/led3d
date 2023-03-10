#!/usr/bin/env python3

import sys
sys.path.append('..')
import src.config as cfg
import src.dbio as db
import src.sim_led as led
import src.utilities as ut

# specify program here
#import programs.bottom_up_wave as prg
#import programs.left_right_right_left as prg
#import programs.sparkling_candles as prg
import programs.traversing_plane as prg

if __name__ == "__main__" :
    
    conn = db.create_connection("/home/philip/Projects/led3d/db/calibinfo.sqlite")

    chain = led.sim_ledchain()
    leds = []
    for id in range(cfg.NLEDs) :
        try :
            (x, y, z) = db.read_led(conn, id)
            leds.append(led.sim_led(id, chain, (x, y, z), (1, 1, 1)))
        except Exception :
            ut.warn("LED", id, " not in database.")
    
    fps = 10
    program = prg.program()
    
    for frame in range(250) :
        t = frame/fps
        program.set_state(t)
        for LED in leds :
            program.set_coordinates(LED.led_id, LED.x, LED.y, LED.z)
            r, g, b = program.get_rgb()
            LED.frame = frame
            LED.set_rgb(r, g, b)
            LED.commit()
