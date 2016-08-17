#!/usr/bin/env python3

from .FalloutObject import FalloutObject
class Armor(FalloutObject):
    no_armor="none"
    light="light"
    medium="medium"
    heavy="heavy"
    power="power"
    custom="custom"

    blocklist={ no_armor: [],
                light: [4],
                medium: [6],
                heavy: [8],
                power: [1,2,4,8,16,32,64,128] }
    
    def __init__(self,name="generic armor",armortype=None,
                 blocks=None,**kwargs):
        super(Armor,self).__init__(**kwargs)
        self.name = name
        if armortype == None or armortype==Armor.custom:
            if blocks==None:
                self.blocks = []
                self.armortype = Armor.no_armor
            else:
                self.blocks = blocks
        else:
            self.armortype = armortype
            try:
                # Don't share the blocklist.
                self.blocks = [ x for x in Armor.blocklist[armortype] ]
            except KeyError:
                raise ArmorException("Unknown armor type %s" % armortype)

    def __str__(self):
        s = "%s (%s): blocks " % (self.name,self.armortype)
        if self.blocks:
            if len(self.blocks) > 1:
                s = s + str(self.blocks)
            else:
                s = s + str(self.blocks[0])
        else:
            s = s + "nothing"
        return s

    def copy(self):
        a=Armor(name=self.name,debug=self.debug,quiet=self.quiet,
                verbose=self.verbose,logger=self.logger)
        a.armortype=self.armortype
        a.blocks = [ x for x in self.blocks ]
        return a
