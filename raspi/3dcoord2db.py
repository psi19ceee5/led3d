#!/usr/bin/env python3

import sqlite3
import sys
sys.path.append('..')
import src.utilities as ut
import math
from scipy.optimize import minimize
import src.dbio as db
import src.config as cfg

class measured_led :
    def __init__(self, uid) :
        self.id = uid
        self.measurement = {} # dictionary: angle -> (x, y)
        
    def add_data(self, angle, ux, uy) :
        self.measurement[angle] = (ux, uy)
        
    def get_data(self) :
        return self.measurement
        
    def __str__(self) :
        count = 0
        empty = ''
        for angle in self.measurement :
            if count == 0 :
                print(f"id {self.id:<5} --- {angle:<5}: ({self.measurement[angle][0]}, {self.measurement[angle][1]})")
            else :
                print(f"{empty:<8} --- {angle:<5}: ({self.measurement[angle][0]}, {self.measurement[angle][1]})")
            count += 1
        return ''
    
def minfunc(x, *args) :
    if len(x) != 2 :
        print("[ERROR]: x has to have a length of 2 in minfunc")
    if len(args) % 2 != 0 :
        print("[ERROR]: something went wrong with the number of parameters in minfunc.")

    n_meas = round(len(args)/2)
    result = 0
    for i in range(n_meas) :
        alpha = args[2*i]*ut.deg2rad
        meas = args[2*i + 1]
        result += (x[0]*math.cos(alpha) + x[1]*math.sin(alpha) - meas)**2
    return math.sqrt(result)
        
if __name__ == "__main__" :
        
    num_leds = cfg.NLEDs

    conn = db.create_connection("../db/calibinfo.sqlite")    
    
    sql_create_leds = """ CREATE TABLE IF NOT EXISTS leds (
                                    led_id INT PRIMARY KEY,
                                    x REAL,
                                    y REAL,
                                    z REAL
                                ); """
    
    db.create_table(conn, sql_create_leds)

    
    measurements = []
    for id in range(num_leds) :
        data, status = db.read_measurement(conn, id)

        if status == False :
            continue

        measurement = measured_led(id)
        for angle in data :
            measurement.add_data(angle[0], angle[2], angle[1]) # angle[2] = x angle[1] = y (switch back in next iteration)
            
        measurements.append(measurement)
        
    #(meter_per_pixel, img_size_x, img_size_y) = db.read_lengthcalib(conn)
    (meter_per_pixel, img_size_x, img_size_y) = (0.0029, 640, 480)
                
    for m in measurements :
        (x, y, z) = (0, 0, 0)
        params = []
        data = m.get_data()
        for angle in data :
            params.append(angle)
            params.append(data[angle][0])
            z += data[angle][1]
        res = minimize(minfunc, [0, 0], args=tuple(params), method='Nelder-Mead', tol=1e-6)
        (x, y) = (res.x[0], res.x[1])
        z /= len(data)
        z = img_size_y - z
        x *= meter_per_pixel
        y *= meter_per_pixel
        z *= meter_per_pixel
        
        if db.create_led(conn, (m.id, x, y, z)) :
            print("Created led number", m.id, "at", x, y, z)
        elif db.update_led(conn, (x, y, z, m.id)) : 
            print("Updated led number", m.id, "at", x, y, z)
        else :
            print("[ERROR]: Led number", ledid,"could not be registered with the database.")
                    
