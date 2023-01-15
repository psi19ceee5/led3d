#!/usr/bin/env python3

import math
import sys
sys.path.append('..')
import src.program as prg
import src.utilities as ut

ut.info("running program \"bottom_up_wave\")

class program(prg.tmpprg) :
    def __init__(self) :
        super().__init__()
        self.phase_r = 0.
        self.phase_g = 60.*ut.deg2rad
        self.phase_b = 120.*ut.deg2rad
                
    def fkt(self) :
        self.r = math.sin(0.5*math.pi*self.t - (math.pi/0.75)*self.z + self.phase_r)**2
        self.g = math.sin(0.5*math.pi*self.t - (math.pi/0.75)*self.z + self.phase_g)**2
        self.b = math.sin(0.5*math.pi*self.t - (math.pi/0.75)*self.z + self.phase_b)**2

