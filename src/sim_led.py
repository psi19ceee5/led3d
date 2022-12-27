#!/usr/bin/env python3
import bpy
import sys
sys.path.append('..')
import src.proto_led as pled
        
class sim_ledchain(pled.proto_ledchain) :
    def __init__(self) :
        super().__init__()
        
    def commit(self) :
        super().commit()
        print("Method 'commit' has no effect for sim_ledchain")
        
    def off(self) :
        super().off()
        print("Method 'off' has no effect for sim_ledchain")
                
class sim_led(pled.proto_led) :
    def __init__(self, id, ledchain, pos=(0, 0, 0), col=(0, 0, 0)) :
        super().__init__(id, ledchain, pos=pos, col=col)
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
        bpy.context.scene.render.fps = 10
        self.frame = 0

    def commit(self) :
        bpy.data.objects['Sphere-' + str(self.led_id)].select_set(True)
        mat = bpy.data.materials["LED-" + str(self.led_id)]
        mat.diffuse_color = (self.r, self.g, self.b, 1)
        mat.keyframe_insert(data_path="diffuse_color", frame=self.frame)
    