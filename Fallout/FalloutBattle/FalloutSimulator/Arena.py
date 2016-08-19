#!/usr/bin/env python3

from .FalloutObject import FalloutObject

class Arena(FalloutObject):
    def __init__(self,name="generic arena", max_x=49,max_y=49,contents=[],
                 **kwargs):
        super(Arena,self).__init__(**kwargs)
        self.name=name
        self.max_x=max_x
        self.max_y=max_y
        self.contents=contents

    def __str__(self):
        s="%s (%dx%d)" % (self.name,self.max_x+1,self.max_y+1)
        if self.verbose:
            for c in self.contents:
                s += "\n  -> %s @ (%d,%d)" % (c.name,c.coordinates.x,
                                              c.coordinates.y)
        return s

    def copy(self):
        a = Arena()
        a.name=self.name
        a.max_x=self.max_x
        a.max_y=self.max_y
        a.debug=self.debug
        a.verbose=self.verbose
        a.quiet=self.quiet
        a.logger=self.logger
        a.contents=[]
        for c in self.contents:
            a.contents.append(c.copy())
        return a
    
    def get_contents_around_point(self,p,rng):
        return [ c for c in self.contents if
                 ( c.coordinates.distance(p) < rng ) ]

