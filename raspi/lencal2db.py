#!/usr/bin/env python3                                                    

import sys
import sqlite3
from sqlite3 import Error
sys.path.append('..')
import src.dbio as db

if __name__ == '__main__':
    value = sys.argv[1]
    
    conn = db.create_connection('../db/calibinfo.sqlite')
    
    sql_create_lengthcalib = """ CREATE TABLE IF NOT EXISTS lengthcalib (
                                        id INT PRIMARY KEY,
                                        meter_per_pixel REAL NOT NULL
                                    ); """
                                    
    db.create_table(conn, sql_create_lengthcalib)
    
    if db.create_lengthcalib(conn, (1, value)) :
        print("Created length calibration", ledid)
    elif db.update_lengthcalib(conn, (value, 1)) : 
        print("Updated length calibration", ledid)
    else :
        print("[ERROR]: Length calibration could not be registered with the database.")
        
    
