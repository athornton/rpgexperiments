#!/usr/bin/env python3

from .FalloutObject import FalloutObject

class Range(FalloutObject):
    pointblank=2
    
    def __init__(self,name='generic range',short=10,medium=25,r_long=50,
                 maximum=100, **kwargs):
        super(Range,self).__init__(**kwargs)
        self.name = name
        self.pointblank=Range.pointblank
        self.short=short
        self.medium=medium
        self.r_long=r_long
        self.maximum=maximum

    def __str__(self):
        s="%s -- PB: %d; S: %d; M: %d; L: %d; X: %d" % ( self.name,
                                                         self.pointblank,
                                                         self.short,
                                                         self.medium,
                                                         self.r_long,
                                                         self.maximum)
        return s

    def copy(self):
        r = Range(name=self.name,short=self.short,medium=self.medium,
                  r_long=self.r_long,maximum=self.maximum,debug=self.debug,
                  verbose=self.verbose,quiet=self.quiet,logger=self.logger)
        return r
    
