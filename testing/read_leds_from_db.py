import sqlite3
import bpy
from ..src import utilities

def create_connection(db_file) :
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e :
        print("[ERROR]:", e)
        
    return conn

def read_led(conn, id) :
    sql = ' SELECT * FROM leds WHERE led_id = ? '
    cur = conn.cursor()
    cur.execute(sql, (id,))
    
    (_, x, y, z) = cur.fetchall()[0]
    
    return (x, y, z)

if __name__ == "__main__" :
    
    conn = create_connection("/home/philip/Projects/led3d/db/calibinfo.sqlite")
    
    for id in range(500) :
        (x, y, z) = read_led(conn, id)
        bpy.ops.mesh.primitive_uv_sphere_add(segments=16, 
                                             ring_count=8, 
                                             radius=0.01, 
                                             enter_editmode=False, 
                                             align='WORLD', 
                                             location=(x, y, z), 
                                             scale=(1, 1, 1))
