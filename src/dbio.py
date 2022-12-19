#!/usr/bin/env python3

import sqlite3
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
    
