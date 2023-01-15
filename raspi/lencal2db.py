#!/usr/bin/env python3                                                    

import sys
import sqlite3
from sqlite3 import Error
sys.path.append('..')
import src.dbio as db
import src.utilities as ut

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
        ut.info("created length calibration with value", value[0])
        ut.info("  image size: (",value[1], value[2],")")
    elif db.update_lengthcalib(conn, (value, 1)) : 
        ut.info("updated length calibration with value", value[0])
        ut.info("  image size: (",value[1], value[2],")")
    else :
        ut.error("length calibration could not be registered with the database.")
        
    
