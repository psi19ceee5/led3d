#!/usr/bin/env python3

import sqlite3
import random as rnd
import math
from sqlite3 import Error

def create_connection(db_file) :
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e :
        print("[ERROR]:", e)
        
    return conn

def create_table(conn, create_table_sql) :
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e :
        print("[ERROR]:", e)

def create_led(conn, data) :
    sql = """ INSERT INTO leds(led_id, x, y, z)
              VALUES(?,?,?,?) """
    try:
        cur = conn.cursor()
        cur.execute(sql, data)
        conn.commit()
    except Error as e :
#        print("[ERROR]:", e)
        return False
        
    return True

def update_led(conn, data) :
    sql = """ UPDATE leds
              SET x = ?,
                  y = ?,
                  z = ?
              WHERE led_id = ? """
    try :
        cur = conn.cursor()
        cur.execute(sql, data)
        conn.commit()
    except Error as e :
        print("[ERROR]: ", e)
        return False
    
    return True

def delete_led(conn, id) :
    sql = ' DELETE FROM leds WHERE id = ? '
    cur = conn.cursor()
    cur.execute(sql, (id,))
    conn.commit()
    
def read_led(conn, id) :
    sql = ' SELECT * FROM leds WHERE led_id = ? '
    cur = conn.cursor()
    cur.execute(sql, (id,))
    
    (_, x, y, z) = cur.fetchall()[0]
    
    return (x, y, z)
    

if __name__ == '__main__':
    conn = create_connection('db/calibinfo.sqlite')
    
    sql_create_leds = """ CREATE TABLE IF NOT EXISTS leds (
                                        led_id INT PRIMARY KEY,
                                        x REAL,
                                        y REAL,
                                        z REAL
                                    ); """
    
    create_table(conn, sql_create_leds)
    
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
        
            if create_led(conn, (ledid, x, y, z)) :
                print("Created led number", ledid)
                ledid += 1
            elif update_led(conn, (x, y, z, ledid)) : 
                print("Updated led number", ledid)
                ledid += 1
            else :
                print("[ERROR]: Led number", ledid,"could not be registered with the database.")