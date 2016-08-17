#!/usr/bin/env python3

from .FalloutObject import FalloutObject
import random

class Die(FalloutObject):
    def __init__(self,sides=6,armor=None,**kwargs):
        super(Die,self).__init__(**kwargs)
        if sides < 1:
            raise DiceException("Invalid number of die sides %d" % sides)
        self.sides=sides
        self.armor=armor
        self.roll()

    def roll(self):
        self.rawrolled=random.randint(1,self.sides)
        self.rolled = self.rawrolled
        self._apply_armor()
        self.log_debug("Rolled: %s" % str(self))

    def _apply_armor(self):
        if not self.armor:
            return
        bl=self.armor.blocklist
        if not bl:
            return
        biggest=max(bl)
        r=self.rawrolled
        if r in bl or ( r == d.sides and biggest > r):
            self.rolled = 0

    def copy(self):
        self.log_debug("Copying die: %s" % self)
        d = Die(sides=self.sides,armor=self.armor,debug=self.debug,
                quiet=self.quiet,verbose=self.verbose,logger=self.logger)
        d.rawrolled = self.rawrolled
        d.rolled = self.rolled
        self.log_debug("Restored rolled values: %s" %d)
        return d
            
    def __str__(self):
        s = "d%d" % self.sides
        if self.debug:
            s +=" [%d]" % self.rolled
            if self.rolled != self.rawrolled:
                s = s + " (was %d before applying armor %s)" % self.armor
        return s

class Dice(FalloutObject):
    def __init__(self,num_dice=1,sides=6,mod=0,**kwargs):
        super(Dice,self).__init__(**kwargs)        
        if num_dice < 1:
            raise DiceException("Invalid number of dice %d" % num_dice)
        self.num_dice=num_dice
        self.sides=sides
        self.dice=[]
        self.mod=mod
        for n in range(num_dice):
            self.dice.append(Die(sides=self.sides,verbose=self.verbose,
                                 debug=self.debug,logger=self.logger))
        self.sum = self._getsum()
        self.total = self._getmod()
        self.log_debug("Rolled: %s" % str(self))

    def __str__(self):
        s="d" + str(self.sides)
        if self.num_dice > 1:
            s = str(self.num_dice) + s
        if self.mod != 0:
            if self.mod < 0:
                s = s + "-" + str(-self.mod)
            else:
                s = s + "+" + str(self.mod)
        if self.debug:
            s += "\nSum: %s Total: %s\n" % (self.sum,self.total)
            for d in self.dice:
                s += " -> %s " % d
        return s

    def _getsum(self):
        sum=0
        for d in self.dice:
            sum=sum+d.rolled
        return sum
    
    def _getmod(self):
        if self.sum == 0:
            return
        total=self.sum
        if self.mod != 0:
            total = total + self.mod
        if total < 0:
            total = 0
        return total

    def _recalc(self):
        self.sum = self._getsum()
        self.total = self._getmod()

    def copy(self):
        self.log_debug("Copying %s..." % self)
        d = Dice(num_dice=self.num_dice,sides=self.sides,mod=self.mod,
                 debug=self.debug,quiet=self.quiet,verbose=self.verbose,
                 logger=self.logger)
        for i in range(self.num_dice):
            d.dice[i] = self.dice[i].copy()
        d._recalc()
        self.log_debug("Restored rolls: %s" % d)
        return d
        
    def roll(self,armor=None):
        for d in self.dice:
            d.roll()
        if armor:
            self.apply_armor
        self._recalc()

    def throw_out_largest(self):
        self.log_debug("Throwing out largest for %s." % str(self))
        dl = []
        for d in self.dice:
            dl.append(d.rolled)
            md = max(dl)
            di = dl.index(md)
            self.dice[di].rolled = 0
            self.dice[di].rawrolled = 0
        self._recalc()
        self.log_debug("After throwing out largest: %s." % str(self))
        
    def apply_armor(self,armor):
        if not armor:
            return
        bl=armor.blocklist
        if not bl:
            return
        biggest=bl[-1]
        for d in self.dice:
            r=d.rawrolled
            d.rolled=r # Reset because armor might have changed
            if r in bl or ( r == d.sides and biggest > r):
                d.rolled = 0
                
