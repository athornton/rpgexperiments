#!/usr/bin/env python3

from .FalloutObject import FalloutObject
from .Special import Special
from .Armor import Armor
from .Strategy import Strategy
from .Arena import Arena
from .Coordinates import Coordinates
from .Skills import Skills
from .Dice import Die
from .Dice import Dice
from .Effect import Effect
from .Faction import Faction
from .Range import Range
from .Weapon import Weapon
from .ActorException import ActorException
import math

class Actor(FalloutObject):
    action_flee="flee"
    action_approach="approach"
    action_retreat="retreat"
    action_attack="attack"
    action_nothing="nothing"
    
    def __init__(self,max_hp=50,max_hp_with_rads=50,current_hp=50,
                 special=None,armor=None,name="generic actor",factions=None,
                 morale=12,effects=None,weapons=None,strategy=None,arena=None,
                 coordinates=None,skills=None,inventory=None,**kwargs):
        super(Actor,self).__init__(**kwargs)
        self.max_hp=max_hp
        self.max_hp_with_rads=max_hp_with_rads
        self.current_hp=current_hp
        self._last_current_hp = current_hp
        self.apply_hp_constraints()
        self._action = None
        self._target = None
        self._weapon = None
        if special == None:
            self.special=Special(debug=self.debug,logger=self.logger,
                                 verbose=self.verbose,quiet=self.quiet)
        else:
            self.special = special
        if armor == None:
            self.armor = Armor(debug=self.debug,logger=self.logger,
                               verbose=self.verbose,quiet=self.quiet)
        else:
            self.armor = armor
        self.name=name
        if factions == None:
            my_fac = Faction(name=self.name,debug=self.debug,
                             logger=self.logger,verbose=self.verbose,
                             quiet=self.quiet)
            self.factions = [ my_fac ]
        self.morale = morale
        if effects == None:
            self.effects = []
        else:
            self.effects = effects
        if strategy == None:
            self.strategy = Strategy(Strategy.melee,debug=self.debug,
                                     logger=self.logger,quiet=self.quiet,
                                     verbose=self.verbose)
        else:
            self.strategy = strategy
        self.weapons=weapons
        if arena == None:
            self.arena = Arena(debug=self.debug,logger=self.logger,
                               verbose=self.verbose,quiet=self.quiet)
        else:
            self.arena = arena
        if self not in self.arena.contents:
            self.arena.contents.append(self)
        if coordinates == None:
            self.coordinates = Coordinates(debug=self.debug,
                                           logger=self.logger,
                                           verbose=self.verbose,
                                           quiet=self.quiet)
        else:
            self.coordinates = coordinates
        if skills == None:
            self.skills= Skills(self,debug=self.debug,
                                logger=self.logger,
                                verbose=self.verbose)
        else:
            self.skills = skills
        if inventory == None:
            self.inventory = []
        else:
            self.inventory = inventory

    def __str__(self):
        s = self.name
        s += "; HP: %d/%d/%d" % (self.current_hp,self.max_hp_with_rads,
                                 self.max_hp)
        s += "\nArmor: %s" % self.armor
        s += "\nWeapon: %s" % self._weapon
        s += "\nAction: %s; " % self._action
        tn = "None"
        if self._target:
            tn = self._target.name
        s += "Target: %s" % tn
        
        if self.verbose:
            s += "\nS.P.E.C.I.A.L.: " + str(self.special)
            s += "\nMorale: %d" % self.morale
            s += "\nArena: %s @ %s" % (self.arena, self.coordinates)
            s += "\nStrategy: %s" % self.strategy
            if self.weapons:
                s += "\n-------\nWeapons:"
                for w in self.weapons:
                    s += "\n%s" % w
            if self.factions:
                s += "\n-------\nFactions:"
                for f in self.factions:
                    s += "\n%s" % f
            if self.inventory:
                s += "\n-------\nInventory: %s" % self.inventory
            s += "\n-------\nSkills:\n%s" % self.skills
        return s

    def copy(self):
        a = Actor(name=self.name, max_hp=self.max_hp,
                  max_hp_with_rads=self.max_hp_with_rads,
                  current_hp=self.current_hp,
                  special=self.special.copy(),
                  armor=self.armor.copy(),
                  morale=self.morale,
                  strategy=self.strategy.copy(),
                  arena=self.arena, # NOTE: not a copy--goes into same arena
                  coordinates=self.coordinates.copy(),
                  skills=self.skills.copy(),
                  quiet=self.quiet,debug=self.debug,verbose=self.verbose,
                  logger=self.logger)
        if self.effects:
            a.effects = [ x.copy() for x in self.effects ]
        if self.weapons:
            a.weapons = [ x.copy() for x in self.weapons ]
        if self.factions:
            a.factions = [ x.copy() for x in self.factions ]
        if self.inventory:
            a.inventory = [ x.copy() for x in self.inventory ]
        a._target = self._target
        a._weapon = self._weapon
        a._action = self._action
        a._last_current_hp = self._last_current_hp
        return a
    
    def get_action(self):
        return self._action

    def get_target(self):
        return self._target

    def get_weapon(self):
        return self._weapon
    
    def apply_hp_constraints(self):
        if self.max_hp_with_rads > self.max_hp:
            self.max_hp_with_rads = self.max_hp
        if self.current_hp > self.max_hp_with_rads:
            self.current_hp = self.max_hp_with_rads

    def flee(self):
        # Just find the nearest edge, and run for it.
        self._action = Actor.action_flee
        shortest=0.0
        dirx="+"
        diry="+"
        axis="x"
        max_x = self.arena.max_x
        max_y = self.arena.max_y
        mid_x = 0.5 * max_x
        mid_y = 0.5 * max_y
        x = self.coordinates.x
        y = self.coordinates.y
        cx=0.0
        cy=0.0
        if x > mid_x:
            cx = max_x - x
        else:
            cx = x
            dirx = "-"
        shortest=cx
        if y > mid_y:
            cy = max_y - y
        else:
            cy = y
            diry = "-"
        if cy < shortest:
            shortest = cy
            axis = "y"
        fleept = Coordinates(debug=self.debug,verbose=self.verbose,
                             logger=self.logger,quiet=self.quiet)
        if axis == "x":
            fleept.y = self.coordinates.y
            if dirx == "+":
                fleept.x = max_x + 1.0
            else:
                fleept.x = -1.0
        else:
            fleept.x = self.coordinates.x
            if diry == "+":
                fleept.y = max_y + 1.0
            else:
                fleept.y = -1.0
        self.move_towards(fleept)
        self.check_coordinate_constraints()

    def check_coordinate_constraints(self):
        max_x = self.arena.max_x
        max_y = self.arena.max_y
        fleeing=False
        if self._action == Actor.action_flee:
            fleeing=True
        c = self.coordinates
        if c.x < 0 or c.y < 0 or c.x > max_x or c.y > max_y:
            if fleeing:
                self.log_debug("%s fled arena %s." % (self.name,
                                                      self.arena.name))
                self._remove_from_arena()
            else:
                self.log_debug("Adjusting %s position %s..." % (self.name,c))
                if c.x < 0:
                    c.x = 0
                if c.y < 0:
                    c.y = 0
                if c.x > max_x:
                    c.x = max_x
                if c.y > max_y:
                    c.y = max_y
                self.log_debug("Adjusted %s position to %s." % (self.name,c))

    def determine_action_with_target(self):
        st = self.strategy.strategy
        if st == Strategy.flee:
            self._action = Actor.action_flee
            return
        if st == Strategy.nothing:
            self._action = Actor.action_nothing
            return
        t = self._target
        if t == None:
            self.action = Actor.action_nothing
            return
        rng = self.coordinates.distance(t.coordinates)
        try:
            self.select_weapon(t)
        except ActorException:
            pass
        # Check again: if we have no ammo and no melee, we set strategy to
        #  flee in select_weapon
        st = self.strategy.strategy
        if st == Strategy.flee:
            self._action = Actor.action_flee
            return
        if not self._weapon:
            self._action = Actor.action_approach
            return
        # Try to close if we're at extreme range
        if self._weapon.w_range and rng > self._weapon.w_range.r_long:
            self._action = Actor.action_approach
            return
        self._action=Actor.action_attack
                            
    def attack(self,actor):
        n = self.name
        if actor.arena != self.arena:
            raise ActorException("'%s' not in same arena as '%s'" % \
                (n, actor.name))
        w = self._weapon
        if not w:
            raise ActorException("'%s' could not select a weapon" % n)
        rng = self.coordinates.distance(actor.coordinates)
        if w.weapontype == Weapon.melee and rng > Range.pointblank:
            raise ActorException("Cannot use weapon '%s' at range '%f" % \
                (w.name, rng))
        self.log("%s attacked %s with %s." % (self.name, actor.name, w.name))
        w.discharge() # Let Exception go: should not have selected empty
        hitchance = self._get_hit_chance(w,actor)
        tohit = Die(100,debug=self.debug,verbose=self.verbose,
                    logger=self.logger,quiet=self.quiet).rolled
        ths = "needed <= %d; rolled %d" % (hitchance,tohit)
        if tohit <= hitchance:
            self.apply_damage(w.damage,actor)
            self.log("Attack (%s) hit: %s -> %s",ths,w.damage,
                     w.damage.get_total_damage())
        else:
            self.log("Attack (%s) missed.",ths)

    def select_target(self):
        # If I already have a target, stick with it if it is still a threat:
        if self._target:
            if self._target.arena == self.arena and \
               self._target.current_hp > 0:
                return
        # For right now, just pick closest unfriendly
        potentials = [ a for a in self.arena.contents if type(a) is Actor \
                       and a != self ]
        hostiles = []
        for p in potentials:
            for f in p.factions:
                skip=False
                for sf in self.factions:
                    if f.name in sf.friendly or f.name in sf.neutral:
                        skip=True
                        break
                if skip:
                    break
            if skip:
                continue
            hostiles.append(p)
        if not hostiles:
            self.log("%s could not choose new target." % self.name)
            return None
        hostiles.sort(key=lambda h: h.coordinates.distance)
        self._target = hostiles[0]
        self.log("%s chose new target %s." % (self.name,self._target.name))
            
    def select_weapon(self,a):
        loaded=[ x for x in self.weapons if
                 (x.weapontype == Weapon.melee or
                  x.ammo_remaining != Weapon.ammo_quantity[0]) ]
        if not loaded:
            # Out of weapons.  Run away
            self.log("%s has no usable weapons; fleeing." % self.name)
            self.strategy.strategy = Strategy.flee
            self._weapon=None
            return None
        noranged = True
        for w in loaded:
            if w.weapontype != Weapon.melee:
                noranged = False
                break
        if noranged and self.strategy.strategy == Strategy.ranged:
            # No ranged attacks left.  Switch to melee.
            self.log("%s has no usable ranged weapons; switching to melee." %
                     self.name)
            self.strategy.strategy = Strategy.melee
        rng = self.coordinates.distance(a.coordinates)
        sortw = sorted(loaded,key=_sort_weapons_by_damage)
        nosplashw = []
        for w in sortw:
            if not w.ammo or w.ammo.splash_radius == 0:
                nosplashw.append(w)
            else:
                sr = w.ammo.get_max_splash()
                in_splash_range = [ a for a in
                                    actor.arena.get_contents_around_point(
                                        actor.coordinates,radius)
                                    if type(a) is Actor ]
                good=True
                for o in in_splash_range:
                    # Refuse weapon if splash might hit friendlies
                    for f in self.factions:
                        if f in o.factions.friendly:
                            self.log_debug("%s rejecting weapon %s (splash)." %
                                           (self.name,w.name))
                            good=False
                            break
                if good:
                    nosplashw.append(w)
        # Now let's figure out which of these weapons, which won't splash to
        #  friendlies, is within range.
        inrange = []
        for w in nosplashw:
            rmax = Range.pointblank
            if w.w_range:
                rmax = w.w_range.maximum
            if w.weapontype == Weapon.thrown:
                rmax = w_range.r_long + 2 * self.special.s
            if rng <= rmax:
                inrange.append(w)
            else:
                self.log_debug("Rejecting weapon %s: out of range." % w.name)
        # Return the last weapon in the list (so the one with the most damage)
        #  if there is one.
        if not inrange:
            self._weapon = None
            self.log("No weapon in range for %s to attack %s" %
                     (self.name,a.name))
            return
        else:
            # We don't update the strategy: we could pick a melee weapon
            #  because the only ranged weapons we have would splash to
            #  friends.
            u=inrange[-1]
            self._weapon = u
            self.log("%s chose weapon %s to attack %s." % (self.name, u.name,
                                                           a.name))
        return

    def getspeed(self):
        # We will need to play with this
        return int(3 + math.ceil( (2.0/3.0) * self.special.a ))
        
    def move_towards(self,c):
        self._move_wrt(c,"towards")

    def move_away(self,c):
        self._move_wrt(c,"away")

    def _move_wrt(self,c,direction):
        if direction != "towards" and direction != "away":
            raise ActorException("Direction '%s' not 'towards' or 'away'" %
                                 direction)
        speed = self.getspeed()
        here = self.coordinates
        dx = c.x - here.x
        dy = c.y - here.y
        rng = here.distance(c)
        if rng <= speed and direction == "towards": # We can get there now
            self.coordinates=c
            return
        cos_vec = dx/rng
        sin_vec = dy/rng
        movex = speed * cos_vec
        movey = speed * sin_vec
        if direction == "away":
            movex = -movex
            movey = -movey
        self.coordinates.x += movex
        self.coordinates.y += movey

    def remove_corpse(self):
        if self.current_hp <= 0:
            self.log("%s is dead; removing from arena %s." %
                     (self.name,self.arena.name))
            # Remove self if dead
            self._remove_from_arena()
        
    def process_turn(self):
        self.check_coordinate_constraints()
        self.remove_corpse()
        if self.arena == None:
            return
        self.select_target()
        self.determine_action_with_target()
        todo = self._action
        t = self._target
        self.log("%s: target is %s; action is %s" % (self.name,t.name,todo))
        if todo == Actor.action_flee:
            self.flee()
        elif todo == Actor.action_nothing:
            pass
        elif todo == Actor.action_retreat:
            self.move_away(t.coordinates)
        elif todo == Actor.action_approach:
            self.move_towards(t.coordinates)           
        elif todo == Actor.action_attack:
            if t.arena == self.arena:
                self.attack(t)
            # If the target has fled or died, it's a no-op.
        else:
            raise ActorException("Invalid action '%s'" % todo)
        
    def apply_damage(self,damage,target):
        d=damage.copy()
        if d.radiation:
            d.radiation.roll(armor=target.armor)
            t=d.radiation.total
            if t > 0:
                target.max_hp_with_rads -= t
                target.apply_hp_constraints()
        if d.physical:
            d.physical.roll(armor=target.armor)
            t = d.physical.total
            if t > 0:
                target.current_hp -= t
        if d.burn:
            d.burn.roll(armor=target.armor)
            t = d.burn.total
            if t > 0:
                target.current_hp -= t
                d.burn.throw_out_largest()
                if d.burn.total > 0:
                    target.effects.append(effecttype=Effect.burn,
                                          effect=d.burn)
        if d.poison:
            d.poison.roll(armor=target.armor)
            if not self.saving_throw("e",d.poisonsavemod):
                t = d.poison.total
                if t > 0:
                    target.current_hp -= t
                    d.poison.throw_out_largest()
                    if d.poison.total > 0:
                        target.effects.append(effecttype=Effect.poison,
                                              effect=d.poison,
                                              poisonsavemod=d.poisonsavemod)
        td = damage.get_total_damage()
        if td != "0":
            my_factions = [ x.name for x in self.factions ]
            self.log("%s did %s damage to %s, causing hostility to %s" %
                     (self.name,td,target.name,my_factions))
            target.faction_anger(my_factions)
        target.check_for_morale_check()

    def check_morale(self):
        c = Dice(sides=6,num_dice=2,verbose=self.verbose,debug=self.debug,
                 logger=self.logger)
        self.log("Morale Check for %s: needed <= than %d, got %d." %
                       (self.name,self.morale,c.total))
        if c.total <= self.morale:
            return True
        return False

    def saving_throw(self,s,mod):
        sp = self.special
        t=0
        if s == "s":
            t = sp.s
        elif s == "p":
            t = sp.p
        elif s == "e":
            t = sp.e
        elif s == "c":
            t = sp.c
        elif s == "i":
            t = sp.i
        elif s == "a":
            t = sp.a
        elif s == "l":
            t = sp.l
        else:
            raise ActorException("Saving throw for invalid attribute '%s'" %s)
        t += mod
        r = Die(10,verbose=self.verbose,logger=self.logger,
                debug=self.debug,quiet=self.quiet).rolled
        self.log("Saving throw against '%s': needed <= %d, got %d." %
                 (s,t,r))
        if r <= t:
            return True
        return False
            
    def faction_anger(self,wounder_factions):
        my_facs = self.factions
        for mf in my_facs:
            if mf.name in wounder_factions:
                self.log("Friendly fire in faction %s." % mf.name)
        for mf in my_facs:
            ff = mf.friendly
            for fff in ff:
                if fff in wounder_factions:
                    self.log("Friendly fire in faction %s." % fff)
                    return
        for mf in my_facs:
            mfn = mf.name
            for wf in wounder_factions:
                mf.neutral = [ x for x in mf.neutral if x != wf ]
                if wf not in mf.hostile:
                    self.log("Faction %s is now hostile to %s" % (mfn,wf))
                    mf.hostile.append(wf)
                else:
                    self.log("Faction %s already hostile to %s" % (mfn,wf))
            
    def apply_splash_damage(self,weapon,target):
        if not weapon or not weapon.ammo or weapon.ammo.splash_radius == 0:
            return
        max_splash = weapon.ammo.get_max_splash()
        tcs = self.arena.get_contents_around_point(target.coordinates,
                                                   max_splash)
        targets = [ x for x in tcs if x is Actor ]
        targets.sort(key=lambda a: a.coordinates.distance(target.coordinates))
        ring=0.0
        dmg = weapon.damage
        for t in targets:
            if t == target:
                continue # intended target doesn't take splash damage
            d = t.coordinates.distance(target.coordinates)
            if d - ring >= 1.0:
                dmg.throw_out_largest()
                ring += 1.0
            self.apply_damage(dmg,t)
            
    def apply_effects(self):
        # A once-per-turn apply-all-current-effects-and-then-decrease-them
        if not self.effects:
            return
        remainder=[]
        for e in self.effects:
            effecttype = e.effecttype
            self.log("Applying ongoing effect %s: %d" %
                     (effecttype,e.effect.total))
            if effecttype == Effect.burn:
                self.current_hp -= e.effect.total
            elif effecttype == Effect.poison:
                if not self.saving_throw("e",Effect.poisonsavemod):
                    self.current_hp -= e.effect.total
            elif effecttype == Effect.heal:
                self.current_hp += e.effect.total
                self.apply_hp_constraints()
            elif effecttype == Effect.healrad:
                self.max_hp_with_rads += e.effect.total
                self.apply_hp_constraints()
                e.effect.throw_out_largest()
            if e.effect.total != 0:
                remainder.append(Effect(effecttype=effecttype,
                                        effect=e.effect,poisonsavemod=
                                        e.effect.poisonsavemod))
        if remainder:
            self.effects=remainder
        else:
            self.effects=None
        self.check_for_morale_check()


    def check_for_morale_check(self):
        # Check morale when first taking damage, or when you hit half HP
        need_morale_check = False
        if self._last_current_hp > self.current_hp:
            if self._last_current_hp == self.max_hp:
                need_morale_check= True
            elif (self._last_current_hp + 0.0) / self.max_hp > 0.5:
                if (self.current_hp + 0.0) / self.max_hp <= 0.5:
                    need_morale_check=True
            self._last_current_hp = self.current_hp
        if need_morale_check:
            if not self.check_morale():
                self._action = Actor.action_flee
                self.strategy.strategy = Strategy.flee
            
    def _get_hit_chance(self,w,a):
        skillname = w.skill
        hitchance = 0
        range_mods = {
            "pointblank": 20,
            "short": 5,
            "medium": 0,
            "long": -20,
            "extreme": -40,
        }
        rng = self.coordinates.distance(a.coordinates)
        # Get appropriate skill
        if skillname == Skills.melee:
            hitchance=self.skills.melee
        elif skillname == Skills.explosives:
            hitchance=self.skills.explosives
        elif skillname == Skills.small_guns:
            hitchance=self.skills.small_guns
        elif skillname == Skills.big_guns:
            hitchance=self.skills.big_guns
        else:
            raise ActorException("Cannot determine skill for weapon '%s'" % \
                                 w.name)
        # Apply range modifier
        rname=""
        if rng <= Range.pointblank:
            rname = "pointblank"
        elif rng <= w.w_range.short:
            rname = "short"
        elif rng <= w.w_range.medium:
            rname = "medium"
        elif rng <= w.w_range.r_long:
            rname = "long"
        else:
            rname = "extreme"
        hitchance += range_mods[rname]
        # Apply target's agility modifier
        hitchance += 10 - ( 2 * a.special.a)
        # 1 always hits, 100 always misses
        if hitchance < 1:
            hitchance = 1
        if hitchance > 99:
            hitchance = 99
        self.log_debug("%s chance to hit %s at range %d with %s: %d." %
                       (self.name,a.name,rng,w.name,hitchance))
        return hitchance

    def _remove_from_arena(self):
        a = self.arena
        self.arena = None
        if a:
            a.contents.remove(self)
            
def _sort_weapons_by_damage(w):
    d = 0
    if w.damage.physical:
        d += w.damage.physical.num_dice * ((1.0 + w.damage.physical.sides) \
                                           / 2 ) + w.damage.physical.mod
    if w.damage.burn:
        d += w.damage.burn.num_dice * ((1.0 + w.damage.physical.sides) \
                                       / 2 ) + w.damage.burn.mod
    if w.damage.radiation:
        d += w.damage.physical.num_dice * ((1.0 + w.damage.radiation.sides) \
                                           / 2 ) + w.damage.radiation.mod
    return d
    
