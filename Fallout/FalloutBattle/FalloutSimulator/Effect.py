#!/usr/bin/env python3

from .FalloutObject import FalloutObject

class Effect(FalloutObject):
    poison="poison"
    burn="burn"
    heal="heal"
    healrad="healrad"
    
    def __init__(self,effecttype="generic effect",effect=None,
                 poisonsavemod=0,**kwargs):
        super(Effect,self).__init__(**kwargs)
        self.effecttype=effecttype
        self.poisonsavemod = poisonsavemod
        self.effect=effect

    def __str__(self):
        return "%s: %s" % (self.effecttype,self.effect)

    def copy(self):
        e=Effect()
        e.effecttype=self.effecttype
        e.poisonsavemod = self.poisonsavemod
        e.effect=self.effect.copy(debug=self.debug,quiet=self.quiet,
                                  verbose=self.verbose,
                                  logger=self.logger)
        e.debug=self.debug
        e.quiet=self.quiet
        e.verbose=self.verbose
        e.logger=self.logger
        return e
    
