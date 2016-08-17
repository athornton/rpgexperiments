#!/usr/bin/env python3
from .FalloutObject import FalloutObject
class Ammo(FalloutObject):
    def __init__(self,name="generic ammo",damage=None,splash_radius=0,
                 **kwargs):
        super(Ammo,self).__init__(**kwargs)
        self.name=name
        self.damage=damage
        self.splash_radius=splash_radius

    def __str__(self):
        s="%s: damage %s" % (self.name,self.damage)
        if self.splash_radius > 0:
            s += " splash radius %dm (max %dm)" % (self.splash_radius,
                                                   self.get_max_splash())
        return s

    def copy(self):
        a = Ammo(name=self.name,splash_radius=self.splash_radius,
                 debug=self.debug,quiet=self.quiet,verbose=self.verbose,
                 logger=self.logger)
        if self.damage:
            a.damage=self.damage.copy()
        return a
    
    def get_max_splash(self):
        if self.splash_radius == 0:
            return 0
        pd = 0
        bd = 0
        rd = 0
        nd = 0
        if self.damage.physical:
            pd = self.damage.physical.num_dice - 1
        if self.damage.burn:
            bd = self.damage.burn.num_dice - 1
        if self.damage.radiation:
            rd = self.damage.radiation.num_dice - 1
        if self.damage.poison:
            nd = self.damage.poison.num_dice - 1
        rmult = max([pd,bd,rd,nd])
        radius = rmult * self.splash_radius
        return radius
