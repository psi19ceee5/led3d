#!/usr/bin/env python3

import math
import numpy as np
import random as rnd
import sys
sys.path.append('..')
import src.program as prg
import src.utilities as ut
import src.config as cfg

class program(prg.tmpprg) :
    def __init__(self) :
        super().__init__()
        self.base_col = (0, 0.5, 0)
        self.candle_col = (1, 1, 0)
        candle_dens = 20
        self.candle_rad = 0.15
        mindist = 0.20
        vol = (cfg.xh - cfg.xl) * (cfg.yh - cfg.yl) * (cfg.zh - cfg.zl)
        ncandles = np.random.poisson(candle_dens*vol)
        
        self.candles = []
        while len(self.candles) < ncandles :
            x = rnd.uniform(cfg.xl, cfg.xh)
            y = rnd.uniform(cfg.yl, cfg.yh)
            z = rnd.uniform(cfg.zl, cfg.zh)
            pos = (x, y, z)
            commit_candle = True
            for can in self.candles :
                if np.linalg.norm(np.array(pos) - np.array(can)) < mindist :
                    commit_candle = False
                    break
            if commit_candle :
                self.candles.append((x, y, z))
                
        self.candle_leds = [None]*len(self.candles)
        print("Number of candles in volume:", len(self.candles))    
        self.leds_checked = []
        
    def set_state(self, t) :
        pass
                
    def fkt(self) :
        pos = (self.x, self.y, self.z)
        iscandle = False
        if self.id in self.candle_leds :
            iscandle = True
        elif not self.id in self.leds_checked :
            for n in range(len(self.candles)) :
                if self.candle_leds[n] == None and np.linalg.norm(np.array(pos) - np.array(self.candles[n])) < self.candle_rad :
                    self.candle_leds[n] = self.id
                    iscandle = True
                    break

        if iscandle :
            self.r, self.g, self.b = self.candle_col
        else :
            self.r, self.g, self.b = self.base_col
            
        if not self.id in self.leds_checked :
            self.leds_checked.append(self.id)

