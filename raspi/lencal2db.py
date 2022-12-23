#!/usr/bin/env python3                                                    

import sys
import sqlite3
from sqlite3 import Error
sys.path.append('..')
import src.dbio as db

if __name__ == '__main__':
    value = sys.argv[1:]
    
    conn = db.create_connection('../db/calibinfo.sqlite')
    
    sql_create_lengthcalib = """ CREATE TABLE IF NOT EXISTS lengthcalib (
                                        id INT PRIMARY KEY,
                                        meter_per_pixel REAL NOT NULL,
                                        img_size_x INT NOT NULL,
                                        img_size_y INT NOT NULL
                                    ); """
                                    
    db.create_table(conn, sql_create_lengthcalib)
    
    if db.create_lengthcalib(conn, (1, value[0], value[1], value[2])) :
        print("Created length calibration with value", value[0])
        print("  image size: (",value[1], value[2],")")
    elif db.update_lengthcalib(conn, (value, 1)) : 
        print("Updated length calibration with value", value[0])
        print("  image size: (",value[1], value[2],")")
    else :
        print("[ERROR]: Length calibration could not be registered with the database.")
        
    
