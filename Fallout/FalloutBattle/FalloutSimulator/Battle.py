#!/usr/bin/env python3

from .Arena import Arena
from .Actor import Actor
from .Coordinates import Coordinates
from .FalloutObject import FalloutObject

class Battle(FalloutObject):
    def __init__(self,name='generic battle',arena=None,**kwargs):
        super(Battle,self).__init__(**kwargs)
        self.name=name
        self.arena=arena
        self._turns=0

    def copy(self):
        b = Battle(name=self.name,arena=self.arena.copy(),debug=self.debug,
                   logger=self.logger,verbose=self.verbose,quiet=self.quiet)
        b._turns = self._turns
        return b

    def get_turns(self):
        return self._turns
    
    def add_actor_at_coords(self,a,c):
        a.arena = self.arena
        a.coordinates = c
        if a not in self.arena.contents:
            self.arena.contents.append(a)

    def remove_actor(a):
        a.arena = None
        if a in self.arena.contents:
            self.arena.contents.remove(a)

    def get_actors(self):
        mid_x=self.arena.max_x * 0.5
        mid_y=self.arena.max_y * 0.5
        middle = Coordinates(mid_x,mid_y)
        size = mid_x + mid_y
        return self.get_actors_within(middle,size)

    def get_actors_within(self,c,d):
        return [ x for x in self.arena.contents if type(x) is Actor and
                 x.coordinates.distance(c) <= d ]
            
    def determine_pacification(self):
        all_actors = self.get_actors()
        factionset = set()
        for a in all_actors:
            for f in a.factions:
                factionset.add(f)
        all_friendly=True
        for a in all_actors:
            for f in factionset:
                fn = set()
                for fnn in a.factions:
                    if fnn.friendly:
                        for x in fnn.friendly:
                            fn.add(x)
                    if fnn.neutral:
                        for x in fnn.neutral:
                            fn.add(x)
                    if f.name not in fn:
                        all_friendly=False
                    break
            if not all_friendly:
                break
        return all_friendly

    def process_turn(self):
        # returns True if Battle is over, False if not
        for a in self.get_actors():
            # Anyone off the map either gets put back on the edge,
            #  or has fled the battle
            a.check_coordinate_constraints()
            a.remove_corpse()
        all_actors=self.get_actors() # Possibly smaller set.
        if self.determine_pacification():
            return True # Battle is over because no one is hostile to
                        #  anyone else (or no one is left)
        actor_list_by_speed=sorted(all_actors,key= lambda n: n.special.a)
        actor_list_by_speed.reverse()
        self._turns += 1
        for a in actor_list_by_speed:
            if a.arena != self.arena:
                # If someone flees or dies during the turn, skip that thing
                continue
            a.process_turn()
        return self.determine_pacification()

    def fight(self):
        done = False
        while not done:
            done=self.process_turn()
        return self.get_actors()
