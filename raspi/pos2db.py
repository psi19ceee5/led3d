#!/usr/bin/env python3                                                     

import sys
import sqlite3
from sqlite3 import Error
sys.path.append('..')
import src.dbio as db
import src.utilities as ut

if __name__ == '__main__':
    led_id = sys.argv[1]
    angle = sys.argv[2]
    i_x = sys.argv[3]
    i_y = sys.argv[4]

    conn = db.create_connection('../db/calibinfo.sqlite')
    
    sql_create_measurements = """ CREATE TABLE IF NOT EXISTS measurements (
                                        led_id INT NOT NULL,
                                        angle REAL NOT NULL,
                                        i_x INT,
                                        i_y INT,
                                        PRIMARY KEY (led_id, angle)
                                    ); """
                                    
    db.create_table(conn, sql_create_measurements)
        
    if db.create_measurement(conn, (led_id, angle, i_x, i_y)) :
        ut.info("created measurement of led number", led_id)
    elif db.update_measurement(conn, (led_id, angle, i_x, i_y)) : 
        ut.info("ppdated measurement of led number", led_id)
    else :
        ut.error("measurement of led number", led_id,"could not be registered with the database.")
    
    
