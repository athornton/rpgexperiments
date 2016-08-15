#!/usr/bin/env python3

from .Skills import Skills
from .Damage import Damage
from .Dice import Die
from .Range import Range
from .WeaponException import WeaponException
from .FalloutObject import FalloutObject
import random

class Weapon(FalloutObject):
    ammo_quantity = [ "none", "1", "2", "3", "some", "plenty", "infinite" ]
    melee="melee"
    thrown="thrown"
    gun="gun"
    heavy="heavy"
    dec_plenty = 20
    dec_some = 6
    
    def __init__(self,name="generic weapon",skill=Skills.melee,
                 weapontype=melee,damage=None,w_range=None,ammo=None,
                 ammo_remaining=None,**kwargs):
        super(Weapon,self).__init__(**kwargs)
        self.name=name
        self.skill=skill
        self.weapontype=weapontype
        self.damage=damage
        self.ammo=ammo
        self.w_range=None
        self.ammo_remaining=None
        if self.w_range == None and self.weapontype != Weapon.melee:
            self.w_range=Range(debug=self.debug,verbose=self.verbose,
                               logger=self.logger)
        if self.weapontype != Weapon.melee:
            if ammo == None:
                raise WeaponException("Weapon type '%s' requires ammo" %
                                      self.weapontype)
            self.ammo=ammo
            self.damage = ammo.damage
            if ammo_remaining==None:
                self.ammo_remaining=Weapon.ammo_quantity[0]
            else:
                if ammo_remaining not in Weapon.ammo_quantity:
                    raise WeaponException("Ammo quantity '%s' none of '%v'" %
                                          (Weapon.ammo_quantity))
                self.ammo_remaining=ammo_remaining

    def __str__(self):
        s = "%s; damage %s" % ( self.name, self.damage)
        if self.verbose:
            s += "; type %s (skill %s)" % (self.weapontype,self.skill)
        if self.ammo:
            s += " Ammo: %s; remaining: %s" % (self.ammo, self.ammo_remaining)
        return s
            
    def discharge(self):
        if self.weapontype == Weapon.melee:
            return # Melee weapons don't use ammunition
        r = self.ammo_remaining
        self.log_debug("Discharging %s: %s (quantity remaining %s)" %
                       (self.name,self.ammo.name,r))
        ri = Weapon.ammo_quantity.index(r)
        if ri ==  0:
            raise WeaponException("No ammunition remaining for %s" %
                                  self.name)
        elif ri < 4 or (r == "some" and Die(Weapon.dec_some).rolled == 1) \
             or (r == "plenty" and Die(Weapon.dec_plenty).rolled == 1):
            self.ammo_remaining=Weapon.ammo_quantity[(ri-1)]
            self.log_debug("Ammo quantity decreased to: %s" %
                           self.ammo_remaining)
        elif r == "infinite" or r=="plenty" or r=="some":
            pass # infinite ammo does not decrease, and we already tried
                 #  decrementing plenty and some.
        else:
            raise WeaponException("Invalid ammo quantity '%s'" % r)
        

    def copy(self):
        ca = None
        if self.ammo:
            ca=self.ammo.copy()
        w = Weapon(name=self.name,skill=self.skill,weapontype=self.weapontype,
                   ammo=ca,ammo_remaining=self.ammo_remaining,
                   debug=self.debug,quiet=self.quiet,
                   verbose=self.verbose,logger=self.logger)
        w.damage = self.damage.copy()
        if self.w_range:
            w.w_range = self.w_range.copy()
        return w
