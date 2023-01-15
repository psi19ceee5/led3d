#!/usr/bin/env python3

import numpy as np
import random as rnd
import sys
sys.path.append('..')
import src.program as prg
import utilities as ut

ut.info("program: left_right_right_left")

class program(prg.tmpprg) :
    def __init__(self) :
        super().__init__()
        self.xl = -0.35
        self.xh = 0.55
        self.vel = 0.3
        self.pos = self.xl
        self.t0 = self.t
        self.col_right = rnd.randint(0, 2)
        self.col_left = (self.col_right + rnd.choice([-1,1])) % 3
        self.colmap = {0: (1, 0, 0), 
                       1: (0, 1, 0), 
                       2: (0, 0, 1),
                       3: (1, 1, 0),
                       4: (0, 1, 1),
                       5: (1, 0, 1),
                       6: (1, 1, 1),
                       7: (1, 0.5, 0.5),
                       8: (0.5, 1, 0.5),
                       9: (0.5, 0.5, 1),
                       10: (1, 0.5, 0),
                       11: (1, 0, 0.5),
                       12: (0.5, 1, 0),
                       13: (0, 1, 0.5),
                       14: (0.5, 0, 1),
                       15: (0, 0.5, 1)}
        self.unused_colors = np.array([])
        self.update_unused_col()
        
    def update_unused_col(self) :
        self.unused_colors = np.arange(0, len(self.colmap))
        self.unused_colors = np.delete(self.unused_colors, np.where(self.unused_colors == self.col_right))
        self.unused_colors = np.delete(self.unused_colors, np.where(self.unused_colors == self.col_left))                                                                    
        
    def set_state(self, t) :
        dt = self.t - self.t0
        self.t0 = self.t
        self.pos += self.vel*dt

        if self.pos > self.xh :
            self.vel *= -1
            self.col_right = self.unused_colors[rnd.randint(0, len(self.unused_colors)-1)]
            self.update_unused_col()
            
        if self.pos < self.xl :
            self.vel *= -1
            self.col_left = self.unused_colors[rnd.randint(0, len(self.unused_colors)-1)]
            self.update_unused_col()
                
    def fkt(self) :            
        if self.x < self.pos :
            self.r, self.g, self.b = self.colmap[self.col_left]
        else:
            self.r, self.g, self.b = self.colmap[self.col_right]
