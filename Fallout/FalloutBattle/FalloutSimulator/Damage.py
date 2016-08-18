#!/usr/bin/env python3
from .FalloutObject import FalloutObject
from .Dice import Dice
class Damage(FalloutObject):
    def __init__(self,physical=None,burn=None,radiation=None,poison=None,
                 poisonsavemod=0,**kwargs):
        super(Damage,self).__init__(**kwargs)
        self.physical = physical
        self.burn = burn
        self.radiation = radiation
        self.poison = poison
        self.poisonsavemod = poisonsavemod
        # Each of the damage types is an instance of Dice.

    def __str__(self):
        s = ""
        something=False
        if self.physical:
            s+="%s " % self.physical
            something=True
        if self.burn:
            s+="Burn: %s " % self.burn
            something=True
        if self.radiation:
            s+="Radiation: %s " % self.radiation
            something=True
        if self.poison:
            s+="Poison: %s " % self.poison
            something=True
        if not something:
            s+="None"
        return s

    def copy(self):
        n=Damage()
        if self.poisonsavemod:
            n.poisonsavemod=self.poisonsavemod
        if self.physical:
            n.physical=self.physical.copy()
        if self.burn:
            n.burn=self.burn.copy()
        if self.radiation:
            n.radiation=self.radiation.copy()
        if self.poison:
            n.poison=self.poison.copy()
        n.debug=self.debug
        n.quiet=self.quiet
        n.verbose=self.verbose
        n.logger=self.logger
        return n

    def roll(self):
        if self.physical:
            self.physical.roll()
        if self.burn:
            self.burn.roll()
        if self.radiation:
            self.radiation.roll()
        if self.poison:
            self.poison.roll()
    
    def throw_out_largest(self):
        self.log_debug("Throwing out largest for %s." % self)
        if self.physical:
            self.physical.throw_out_largest()
            if self.physical.total == 0:
                self.log_debug("Physical damage decreased to 0.")
                self.physical = None
        if self.burn:
            self.burn.throw_out_largest()
            if self.burn.total == 0:
                self.log_debug("Burn damage decreased to 0.")
                self.burn = None
        if self.radiation:
            self.radiation.throw_out_largest()           
            if self.radiation.total == 0:
                self.log_debug("Radiation damage decreased to 0.")
                self.radiation = None
        if self.poison:
            self.poison.throw_out_largest()
            if self.poison.total == 0:
                self.log_debug("Poison damage decreased to 0.")
                self.poison = None
        self.log_debug("Threw out largest for %s." % self)
                
    def get_total_damage(self):
        s=""
        if self.physical:
            t = self.physical.total
            if t > 0:
                s = str(t)
        if self.burn:
            t = self.burn.total
            if t > 0:
                if s:
                    s += " + "
                s += str(self.burn.total) + "B"
        if self.radiation:
            t = self.radiation.total
            if t > 0:
                if t:
                    s += " + "
                s += str(self.radiation.total) + "R"
        if self.poison:
            t = self.poison.total
            if t > 0:
                if s:
                    s += " + "
                s += str(self.poison.total) + "P"
        if s == "":
            s = "0"
        return s
