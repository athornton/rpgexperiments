#!/usr/bin/env python3

from .FalloutObject import FalloutObject
class Special(FalloutObject):
    def __init__(self,s=5,p=5,e=5,c=5,i=5,a=5,l=5,**kwargs):
        super(Special,self).__init__(**kwargs)
        self.s = s
        self.p = p
        self.e = e
        self.c = c
        self.i = i
        self.a = a
        self.l = l

    def __str__(self):
        s = "S: %d; P: %d; E: %d; C: %d; I: %d; A:; %d; L: %d" % ( self.s,
                                                                   self.p,
                                                                   self.e,
                                                                   self.c,
                                                                   self.i,
                                                                   self.a,
                                                                   self.l)
        return s

    def copy(self):
        s = Special(s=self.s,p=self.p,e=self.e,c=self.c,i=self.i,a=self.a,
                    l=self.l,debug=self.debug,verbose=self.verbose,
                    quiet=self.quiet,logger=self.logger)
        return s
