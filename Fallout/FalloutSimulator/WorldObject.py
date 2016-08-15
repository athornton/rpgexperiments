#!/usr/bin/env python3
from .FalloutObject import FalloutObject
from .Coordinates import Coordinates
class WorldObject(FalloutObject):
    def __init__(self,name='generic world object',arena=None,
                 coordinates=None,**kwargs):
        super(WorldObject,self).__init__(**kwargs)
        self.name=name
        self.arena=arena
        self.coordinates=coordinates
        if self.arena:
            if self not in self.arena.contents:
                self.arena.contents.append(self)
        if not self.coordinates:
            self.coordinates=Coordinates(debug=self.debug,quiet=self.quiet,
                                         verbose=self.verbose,
                                         logger=self.logger)
            
    def __str__(self):
        s = self.name
        if self.arena:
            s += " [arena %s" % self.arena.name
            if self.coordinates:
                s += " @%s" % self.coordinates
            s += "]"
        return s

    def _remove_from_arena(self):
        a = self.arena
        self.arena = None
        if a:
            a.contents.remove(self)

    def copy(self):
        w=WorldObject(debug=self.debug,quiet=self.quiet,verbose=self.verbose,
                      logger=self.logger)
        w.name=self.name
        w.arena=self.arena # Not a copy
        w.coordinates = self.coordinates.copy()
        return w
    
    
