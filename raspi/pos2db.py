#!/usr/bin/env python3                                                     

import sys
import sqlite3
from sqlite3 import Error
sys.path.append('..')
import src.dbio as db

if __name__ == '__main__':
    angle = sys.argv[1]
    i_x = sys.argv[2]
    i_y = sys.argv[3]

    conn = db.create_connection('db/calibinfo.sqlite')
    
    sql_create_measurements = """ CREATE TABLE IF NOT EXISTS measurements (
                                        led_id INT NOT NULL
                                        angle REAL NOT NULL
                                        i_x INT
                                        i_y INT
                                        PRIMARY KEY (led_id, angle)
                                    ); """
                                    
    db.create_table(conn, sql_create_measurements)
    
    db.create_measurement(conn, (angle, i_x, i_y))
