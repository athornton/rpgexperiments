#!/usr/bin/env python3
from .FalloutObject import FalloutObject
class Faction(FalloutObject):
    def __init__(self,name="generic faction", friendly=[],neutral=[],
                 hostile=[],**kwargs):
        super(Faction,self).__init__(**kwargs)
        self.name = name
        self.friendly = friendly
        if not self.friendly:
            self.friendly = [ name ] # Factions are friendly to themselves.
        self.neutral = neutral
        self.hostile = hostile
        
    def __str__(self):
        s = "%s" % self.name
        sf = [ x for x in self.friendly if x != self.name ]
        if sf:
            s += "; friendly to %s" % sf
        if self.neutral:
            s += "; neutral to %s" % self.neutral
        if self.hostile:
            s += "; hostile to %s" % self.hostile
        return s

    def copy(self):
        f = Faction(name=self.name,friendly = [ x for x in self.friendly ],
                    neutral = [ x for x in self.neutral],
                    hostile = [ x for x in self.hostile], debug=self.debug,
                    quiet=self.quiet, verbose=self.verbose, logger=self.logger)
        return f
