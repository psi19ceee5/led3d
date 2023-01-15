#!/usr/bin/env python3

import math
import random as rnd
import numpy as np
from scipy.spatial.transform import Rotation as rot
import sys
sys.path.append('..')
import src.program as prg
import src.utilities as ut
import src.config as cfg

class program(prg.tmpprg) :
    def __init__(self) :
        super().__init__()
        self.xl = cfg.xl
        self.xh = cfg.xh
        self.yl = cfg.yl
        self.yh = cfg.yh
        self.zl = cfg.zl
        self.zh = cfg.zh
        self.rmax = max(self.xh - self.xl, self.yh - self.yl, self.zh -self.zl)
        self.rmax /= math.sqrt(2)
        self.vel = 0.3
        self.pos = -1*self.rmax
        self.width = 0.05
        self.t0 = self.t
        self.alpha = rnd.uniform(0, 360)
        self.beta = rnd.uniform(0, 360)
        self.gamma = rnd.uniform(0, 360) # actually not neccessary since planes are z-rot invariant
        self.rot = rot.from_euler('xyz', [self.alpha, self.beta, self.gamma], degrees=True)
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
        self.ncolors = len(self.colmap)
        self.currentcol = rnd.randint(0, self.ncolors - 1)
        self.unused_colors = np.array([])
        self.update_unused_col()
        
    def update_unused_col(self) :
        self.unused_colors = np.arange(0, len(self.colmap))
        self.unused_colors = np.delete(self.unused_colors, np.where(self.unused_colors == self.currentcol))

    def set_state(self, t) :
        self.t = t
        dt = self.t - self.t0
        self.t0 = self.t
        self.pos += self.vel*dt
        
        if self.pos > self.rmax :
            self.pos = -1*self.rmax
            self.alpha = rnd.uniform(0, 360)
            self.beta = rnd.uniform(0, 360)
            self.gamma = rnd.uniform(0, 360) # actually not neccessary since planes are z-rot invariant
            self.rot = rot.from_euler('xyz', [self.alpha, self.beta, self.gamma], degrees=True)
            self.currentcol = self.unused_colors[rnd.randint(0, len(self.unused_colors)-1)]
            self.update_unused_col()

                
    def fkt(self) :
        self.z -= (self.zh - self.zl)/2. # place rotation center at center of tree
        x_, y_, z_ = self.rot.apply(np.array([self.x, self.y, self.z]))
        print(z_, " -- ", self.pos)
        if z_ > self.pos - self.width and z_ < self.pos + self.width :
            self.r, self.g, self.b = self.colmap[self.currentcol]
        else :
            self.r, self.g, self.b = (0, 0, 0)
