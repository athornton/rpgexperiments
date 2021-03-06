#!/usr/bin/env python3

from .FalloutObject import FalloutObject
class Skills(FalloutObject):
    melee="melee"
    small_guns="small guns"
    big_guns="big guns"
    explosives="explosives"
    repair="repair"
    lockpick="lockpick"
    science="science"
    speech="speech"
    medic="medic"
    sneak="sneak"
    observe="observe"

    def __init__(self,name='generic skills',actor=None,**kwargs):
        super(Skills,self).__init__(**kwargs)
        self.name = name
        if actor == None or actor.special==None:
            self.melee = 30
            self.small_guns = 30
            self.big_guns = 30
            self.explosives = 30
            self.repair = 30
            self.lockpick = 30
            self.science = 30
            self.speech = 30
            self.medic = 30
            self.sneak = 30
            self.observe = 30
        else:
            self.recalc(actor.special)

    def __str__(self):
        s =  "Melee:      %d\n" % self.melee
        s += "Small Guns: %d\n" % self.small_guns
        s += "Big Guns:   %d\n" % self.big_guns
        s += "Explosives: %d\n" % self.explosives
        s += "Repair:     %d\n" % self.repair
        s += "Lockpick:   %d\n" % self.lockpick
        s += "Science:    %d\n" % self.science
        s += "Medic:      %d\n" % self.medic
        s += "Sneak:      %d\n" % self.sneak
        s += "Observe:    %d"   % self.observe
        return s

    def copy(self):
        s = Skills()
        s.name=self.name
        s.melee=self.melee
        s.small_guns=self.small_guns
        s.big_guns=self.big_guns
        s.explosives=self.explosives
        s.repair=self.repair
        s.lockpick=self.lockpick
        s.science=self.science
        s.medic=self.medic
        s.sneak=self.sneak
        s.observe=self.observe
        s.debug=self.debug
        s.verbose=self.verbose
        s.quiet=self.quiet,
        s.logger=self.logger
        return s
    
    def recalc(self,sp):
        l = sp.l
        self.melee = int(l + 5 * sp.s)
        self.small_guns = int(l + 5 * sp.a)
        self.big_guns = int(l + 5 * ( sp.e + sp.a ) / 2)
        self.explosives = int(l + 5 * (sp.a + sp.p ) / 2)
        self.repair = int(l + 5 * (sp.i + sp.a) / 2)
        self.lockpick = int(l + 5 * (sp.i + sp.a) / 2)
        self.science = int(l + 5 * sp.i)
        self.speech = int(l + 5 * sp.c)
        self.medic = int(l + 5 * (sp.i + sp.c) / 2)
        self.sneak = int(l + 5 * sp.a)
        self.observe = int(l + 5 * sp.p)
