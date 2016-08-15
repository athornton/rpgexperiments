#!/usr/bin/env python3

from .FalloutObject import FalloutObject
import math

class Coordinates(FalloutObject):
    def __init__(self,x=0,y=0,**kwargs):
        super(Coordinates,self).__init__(**kwargs)
        self.x=x
        self.y=y

    def __str__(self):
        return "(" + str(self.x) + "," + str(self.y) + ")"

    def distance(self,c2):
        dx = self.x - c2.x
        dy = self.y - c2.y
        return math.sqrt( (dx * dx) + (dy * dy))

    def copy(self):
        c = Coordinates(x=self.x,y=self.y,logger=self.logger,debug=self.debug,
                        quiet=self.quiet,verbose=self.verbose)
        return c
