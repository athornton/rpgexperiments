#!/usr/bin/env python3
from .WorldObject import WorldObject

class Item(WorldObject):
    def __init__(self,name='generic item',
                 description='generic item description', weight=0,
                 bulk=0, **kwargs):
        super(Item,self_).__init__(**kwargs)
        self.name=name,
        self.description=description,
        self.weight=weight,
        self.bulk=bulk

    def __str__(self):
        s="%s: %s [ weight %d, bulk %d ]" % (self.name,self.description,
                                             self.weight, self.bulk)
        return s

    def copy(self):
        i=Item(name=self.name,description=self.description,weight=self.weight,
               bulk=self.bulk,arena=self.arena,
               coordinates=self.coordinates.copy(),
               debug=self.debug,verbose=self.verbose,quiet=self.quiet,
               logger=self.logger)
        return i
    
