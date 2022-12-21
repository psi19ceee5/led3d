#!/usr/bin/env python3

import abc
from abc import ABC, abstractmethod

# implementations of proto_led should expect pos in meter and col in range [0,1]

class proto_led(ABC) :
    def __init__(self, id, pos=(0, 0, 0), col=(0, 0, 0)) :
        self.led_id = id
        (self.x, self.y, self.z) = pos
        (self.r, self.g, self.b) = col
        
    def set_xyz(self, ux, uy, uz) :
        (self.x, self.y, self. z) = (ux, uy, uz)

    def set_rgb(self, ur, ug, ub) :
        (self.r, self.g, self. b) = (ur, ug, ub)
        
    def get_xyz(self) :
        return self.x, self.y, self.z
    
    def get_rgb(self) :
        return self.r, self.y, self.z
               
    # implementation depends on use case: real-world application or simulation
    @abstractmethod
    def commit(self) :
        pass
    
    

