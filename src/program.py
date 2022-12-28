#!/usr/bin/env python3

import abc
from abc import ABC, abstractmethod

class tmpprg(ABC) :
    @abstractmethod
    def __init__(self) :
        self.x = 0
        self.y = 0
        self.z = 0
        self.t = 0
        self.r = 0
        self.g = 0
        self.b = 0
        self.id = 0
        
    @abstractmethod
    def fkt(self) :
        pass
    
    def set_coordinates(self, id, x, y, z, t) :
        self.id = id
        self.x = x
        self.y = y
        self.z = z
        self.t = t
        
    def set_state(self, t):
        pass
    
    def get_rgb(self) :
        self.fkt()
        return self.r, self.g, self.b
    