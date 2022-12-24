#!/usr/bin/env python3

import sqlite3
import sys
import math
import numpy as np
sys.path.append('..')
import src.config as cfg
import src.dbio as db
import src.led as led

class db_led(led.proto_led) :
    def commit(self, conn) :
        db.update_led(conn, (self.x, self.y, self.z, self.led_id))

if __name__ == "__main__" :
    
    #upper bounds on tree radius and height
    tree_radius = 1.
    tree_height = 2.
    
    conn =  db.create_connection("../db/calibinfo.sqlite")

    leds = []
    for id in range(cfg.NLEDs) :
        try :
            (x, y, z) = db.read_led(conn, id)
            leds.append(db_led(id, pos=(x, y, z)))
        except Exception :
            print("[ERROR]:", Exception)
        
    failstat = [0]*len(leds)
    for n in range(len(leds)) :
        led = leds[n]
        rho = math.sqrt(led.x**2 + led.y**2)
        rcone = tree_radius * (1. - led.z/tree_height)
        if rho > rcone :
            failstat[n] = 1
            
    for n in range(len(leds)) :
        if n == 0 or n == len(leds) :
            continue
        if failstat[n] and not failstat[n-1] and not failstat[n+1] :
            led0 = leds[n-1]
            led1 = leds[n+1]
            pos0 = np.array([led0.x, led0.y, led0.z])
            pos1 = np.array([led1.x, led1.y, led1.z])
            diff = pos1 - pos0
            intpos = pos0 + 0.5*diff
            print("correcting postion of led ", leds[n].led_id, leds[n].x, leds[n].y, leds[n].z, "->", intpos[0], intpos[1], intpos[2])
            leds[n].set_xyz(intpos[0], intpos[1], intpos[2])
            leds[n].commit(conn)
            
    
        