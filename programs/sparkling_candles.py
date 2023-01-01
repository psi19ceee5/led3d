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
        self.base_col = (0, 0.3, 0)
        self.candle_col = (1, 1, 0)
        candle_dens = 60
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
                
        self.candle_leds = np.array([None]*len(self.candles))
        print("Number of candles in volume:", len(self.candles))
        self.candle_brightness = np.array([1]*len(self.candles))
        self.leds_checked = []
        self.t0 = 0

        self.hasShootingStar = False
        self.ssProb = 1.
        self.ssVel = 1.
        self.ssZenith = 0
        self.ssAzimuth = 0
        self.ssStart = np.array([0, 0, 0])
        self.ssPos = np.array([0, 0, 0])
        self.ssDir = np.array([0, 0, -1])
        self.ssRadius = 0.10
        
    def brightness_fkt(self, dt, b0) :
        b0 *= 1000
        pull = 0.3
        db = pull*(1000-b0)
        lam = 2*dt
        dimm = 300*np.random.uniform(0,1,len(self.candles))*np.random.poisson(lam,len(self.candles))
        bright = b0 - dimm + db
        bright = bright * (bright > 0).astype(int)
        bright /= 1000
        return bright
        
    def set_state(self, t) :
        dt = 0
        if self.t0 > 0 :
            dt = t - self.t0
            self.candle_brightness = self.brightness_fkt(dt, self.candle_brightness)
        self.t0 = t
        
        if self.hasShootingStar :
            # 5. update position of star according to vec_pos1 = vec_pos0 + vec_v*dt
            self.ssPos += self.ssVel*dt*self.ssDir
            if self.ssPos[2] < 0 :
                self.hasShootingStar = False
        else :
            # if no shooting star exists: roll dice
            if self.ssProb*dt > rnd.random() :
                self.hasShootingStar = True
                # find trajectory and initial state of shooting star
                # 1. random pivot point within tree-cube
                #pivot = np.array([rnd.uniform(cfg.xl, cfg.xh), rnd.uniform(cfg.yl, cfg.yh), rnd.uniform(cfg.zl, cfg.zh)])
                pivot = np.array([0, 0, cfg.zh - 0.1])
                # 2. random zenith angle between 0 and 60 deg and random azimuth angle between 0 and 360 deg
                self.ssZenith = rnd.uniform(30*ut.deg2rad, 45*ut.deg2rad)
                self.ssAzimuth = rnd.uniform(0, 360*ut.deg2rad)
                # 3. parameterize curve: starting at top-intersection and ending with ground-intersection:
                #    at t0, star starts at height, propagages with v
                hyp = math.tan(self.ssZenith)*(cfg.zh - pivot[2])
                xstart = pivot[0] + math.cos(self.ssAzimuth)*hyp
                ystart = pivot[1] + math.sin(self.ssAzimuth)*hyp
                zstart = cfg.zh
                # 4. write curve-parameters and current position of shooting star to member variables
                self.ssStart = np.array([xstart, ystart, zstart])
                self.ssPos = self.ssStart
                self.ssDir = (pivot - self.ssStart)
                self.ssDir /= np.linalg.norm(self.ssDir)

        print(self.ssPos)                
        
                
    def fkt(self) :
        pos = (self.x, self.y, self.z)
        iscandle = False
        bright = 1.
        if self.id in self.candle_leds :
            iscandle = True
            bright = self.candle_brightness[np.where(self.candle_leds == self.id)[0][0]]
        elif not self.id in self.leds_checked :
            for n in range(len(self.candles)) :
                if self.candle_leds[n] == None and np.linalg.norm(np.array(pos) - np.array(self.candles[n])) < self.candle_rad :
                    self.candle_leds[n] = self.id
                    iscandle = True
                    break
                
        if iscandle :
            self.r, self.g, self.b = (x*bright for x in self.candle_col)
        else :
            self.r, self.g, self.b = self.base_col
            
        if not self.id in self.leds_checked :
            self.leds_checked.append(self.id)
            
        # check if led is close to shooting star and override col = (1, 1, 1)
        dist_2_ss = np.linalg.norm(np.array(pos) - self.ssPos)
        if self.hasShootingStar and dist_2_ss < self.ssRadius :
            self.r, self.g, self.b = (1, 1, 1)

