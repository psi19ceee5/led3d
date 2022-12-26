import sqlite3
import bpy
import sys
import math
sys.path.append('..')
import src.config as cfg
import src.dbio as db
import src.led as led

class sim_led(led.proto_led) :
    def __init__(self, id, pos=(0, 0, 0), col=(0, 0, 0)) :
        super().__init__(id, pos=pos, col=col)
        bpy.ops.mesh.primitive_uv_sphere_add(segments=16, 
                                             ring_count=8, 
                                             radius=0.01, 
                                             enter_editmode=False, 
                                             align='WORLD', 
                                             location=(self.x, self.y, self.z), 
                                             scale=(1, 1, 1))
        ob = bpy.context.active_object
        ob.name = "Sphere-" + str(self.led_id)
        mat = bpy.data.materials.new(name="LED-" + str(self.led_id))
        mat.diffuse_color = (self.r, self.g, self.b, 1)
        # Assign it to object
        if ob.data.materials:
            # assign to 1st material slot
            ob.data.materials[0] = mat
        else:
            # no slots
            ob.data.materials.append(mat)
        self.frame = 0

    def commit(self) :
        bpy.data.objects['Sphere-' + str(self.led_id)].select_set(True)
        ob = bpy.context.active_object
        mat = bpy.data.materials["LED-" + str(self.led_id)]
        mat.diffuse_color = (self.r, self.g, self.b, 1)
        mat.keyframe_insert(data_path="diffuse_color", frame=self.frame)
        

if __name__ == "__main__" :
    
    conn = db.create_connection("/home/philip/Projects/led3d/db/calibinfo.sqlite")

    leds = []
    for id in range(cfg.NLEDs) :
        try :
            (x, y, z) = db.read_led(conn, id)
            leds.append(sim_led(id, (x, y, z), (1, 1, 1)))
        except Exception :
            print("[ERROR]: LED", id, " not in database.")
    
    fps = 25
    phase_r = 0
    phase_g = 60*math.pi/180.
    phase_b = 120*math.pi/180.
    for frame in range(250) :
        for led in leds :            
            r = math.sin(0.5*math.pi*(frame/fps) - (math.pi/0.25)*led.z + phase_r)**2
            g = math.sin(0.5*math.pi*(frame/fps) - (math.pi/0.25)*led.z + phase_g)**2
            b = math.sin(0.5*math.pi*(frame/fps) - (math.pi/0.25)*led.z + phase_b)**2
            led.frame = frame
            led.set_rgb(r, g, b)
            led.commit()
