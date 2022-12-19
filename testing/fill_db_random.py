#!/usr/bin/env python3

import random as rnd
import math
import sys
sys.path.append('..')
import src.dbio as db


if __name__ == '__main__':
    conn = db.create_connection('db/calibinfo.sqlite')
    
    sql_create_leds = """ CREATE TABLE IF NOT EXISTS leds (
                                        led_id INT PRIMARY KEY,
                                        x REAL,
                                        y REAL,
                                        z REAL
                                    ); """
    
    db.create_table(conn, sql_create_leds)
    
    tree_height = 1.5
    tree_maxrad = 0.8
    ledid = 0
    while ledid < 500 :
        rndrho = rnd.uniform(0, tree_maxrad)
        rndrho_ = rnd.uniform(0, tree_maxrad) # dummy variable to obtain a linearly growing probability
        rndphi = rnd.uniform(0, 2*math.pi)
        rndz = rnd.uniform(0, tree_height)
        
        if rndz < (tree_height - (tree_height/tree_maxrad)*rndrho) and rndrho_ < rndrho :
            x = rndrho * math.cos(rndphi)
            y = rndrho * math.sin(rndphi)
            z = rndz
        
            if db.create_led(conn, (ledid, x, y, z)) :
                print("Created led number", ledid)
                ledid += 1
            elif db.update_led(conn, (x, y, z, ledid)) : 
                print("Updated led number", ledid)
                ledid += 1
            else :
                print("[ERROR]: Led number", ledid,"could not be registered with the database.")