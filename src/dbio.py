#!/usr/bin/env python3

import sqlite3
from sqlite3 import Error
import numpy as np
import sys
sys.path.append('..')
import src.utilities as ut

def create_connection(db_file) :
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e :
        ut.error("(create_connection):", e)
        
    return conn

def create_table(conn, create_table_sql) :
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e :
        ut.error("(create_table):", e)
        
# db table 'measurements'
def create_measurement(conn, data) :
    sql = """ INSERT INTO measurements (led_id, angle, i_x, i_y)
              VALUES(?,?,?,?) """
    try:
        cur = conn.cursor()
        cur.execute(sql, data)
        conn.commit()
    except Error as e :
        # ut.error(e)
        return False
        
    return True

def delete_measurement_angle(conn, angle) :
    sql = ' DELETE FROM measurements WHERE angle = ? '
    cur = conn.cursor()
    cur.execute(sql, (angle,))
    conn.commit()    

def delete_measurement_id(conn, id) :
    sql = ' DELETE FROM measurements WHERE led_id = ? '
    cur = conn.cursor()
    cur.execute(sql, (id,))
    conn.commit()  
    
def read_measurement(conn, id) :
    sql = ' SELECT * FROM measurements WHERE led_id = ? '
    cur = conn.cursor()
    cur.execute(sql, (id,))
    
    rows = np.array(cur.fetchall())

    if len(np.shape(rows)) == 2 :
        return rows[:,1:], True
    elif len(np.shape(rows)) == 1 :
        return rows[1:], False
    else :
        return None, False
    
# db table 'led'
def create_led(conn, data) :
    sql = """ INSERT INTO leds (led_id, x, y, z)
              VALUES(?,?,?,?) """
    try:
        cur = conn.cursor()
        cur.execute(sql, data)
        conn.commit()
    except Error as e :
#        ut.error(e)
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
        ut.error(e)
        return False
    
    return True

def delete_led(conn, id) :
    sql = ' DELETE FROM leds WHERE led_id = ? '
    cur = conn.cursor()
    cur.execute(sql, (id,))
    conn.commit()
    
def read_led(conn, id) :
    sql = ' SELECT * FROM leds WHERE led_id = ? '
    cur = conn.cursor()
    cur.execute(sql, (id,))
    
    (_, x, y, z) = cur.fetchall()[0]
    
    return (x, y, z)

# db table 'lengthcalib'
def create_lengthcalib(conn, data) :
    sql = """ INSERT INTO lengthcalib (id, meter_per_pixel, img_size_x, img_size_y)
              VALUES(?, ?, ?, ?) """
    try :
        cur = conn.cursor()
        cur.execute(sql, data)
        conn.commit()
    except Error as e :
        ut.error(e)
        return False
    
    return True

def delete_lengthcalib(conn, id) :
    sql = ' DELETE FROM lengthcalib WHERE id = ? '
    cur = conn.cursor()
    cur.execute(sql, (id,))
    conn.commit()
    
def update_lengthcalib(conn, data) :   
    sql = """ UPDATE lengthcalib
              SET meter_per_pixel = ?,
              SET img_size_x = ?,
              SET img_size_y = ?,
              WHERE id = 1 """
    try :
        cur = conn.cursor()
        cur.execute(sql, data)
        conn.commit()
    except Error as e :
        ut.error(e)
        return False
    
    return True
    
def read_lengthcalib(conn) :
    sql = ' SELECT * FROM lengthcalib WHERE id = ? '
    cur = conn.cursor()
    cur.execute(sql, (1,))
    
    (_, meter_per_pixel, width_px, height_px) = cur.fetchall()[0]
    
    return (meter_per_pixel, width_px, height_px)
