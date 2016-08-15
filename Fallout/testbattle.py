#!/usr/bin/env python3

import FalloutSimulator
import logging

debug=False
verbose=False
quiet=False

lgr=logging.getLogger(name="Battle")
lgr.setLevel(logging.DEBUG)
ch=logging.StreamHandler()
ch.setLevel(logging.DEBUG)
lgr.addHandler(ch)
ar = FalloutSimulator.Arena.Arena(name='Arena 1',logger=lgr)
bt = FalloutSimulator.Battle.Battle(name='Battle',arena=ar,logger=lgr,
                                    debug=debug,verbose=verbose,quiet=quiet)
r1 = FalloutSimulator.Actor.Actor(name="Raider 1",arena=ar,logger=lgr,
                                  debug=debug,verbose=verbose,quiet=quiet)
ww=FalloutSimulator.Weapon.Weapon
wd=FalloutSimulator.Damage.Damage
wdmg=wd(physical=FalloutSimulator.Dice.Dice(num_dice=1,sides=6,
                                            logger=lgr,
                                            debug=debug,
                                            verbose=verbose,
                                            quiet=quiet))
gun=ww(name=".38 pistol",
       weapontype=FalloutSimulator.Weapon.Weapon.gun,
       w_range=FalloutSimulator.Range.Range(),
       skill=FalloutSimulator.Skills.Skills.small_guns,
       ammo=FalloutSimulator.Ammo.Ammo(name=".38",damage=wdmg),
       ammo_remaining=FalloutSimulator.Weapon.Weapon.ammo_quantity[5],
       logger=lgr,debug=debug,verbose=verbose,quiet=quiet)
knife=ww(name="combat knife",
         weapontype=FalloutSimulator.Weapon.Weapon.melee,
         skill=FalloutSimulator.Skills.Skills.melee,
         damage=wdmg.copy(),
         logger=lgr,debug=debug,verbose=verbose,quiet=quiet)
r1armor=FalloutSimulator.Armor.Armor(name='Raider leathers',armortype=
                                     FalloutSimulator.Armor.Armor.light,
                                     logger=lgr,verbose=verbose,debug=debug,
                                     quiet=quiet)
st1=FalloutSimulator.Strategy.Strategy(FalloutSimulator.Strategy.\
                                       Strategy.ranged,logger=lgr,
                                       verbose=verbose,debug=debug,
                                       quiet=quiet)
r1.strategy=st1
r1.weapons=[gun,knife]
r1.armor=r1armor
r1.skills.small_guns = 50
r1.skills.melee = 50
r1.coordinates=FalloutSimulator.Coordinates.Coordinates(10,10,
                                                        logger=lgr,
                                                        debug=debug,
                                                        verbose=verbose,
                                                        quiet=quiet)
r1.morale = 8

# Now make a copy, only in the other corner, and mutually hostile
r2=r1.copy()
r2.name = 'Raider 2'
r2.coordinates=FalloutSimulator.Coordinates.Coordinates(40,40,
                                                        logger=lgr,
                                                        debug=debug,
                                                        verbose=verbose,
                                                        quiet=quiet)
newfac = FalloutSimulator.Faction.Faction(name=r2.name,
                                          logger=lgr,
                                          debug=debug,
                                          verbose=verbose,
                                          quiet=quiet)
r2.factions = [ newfac ]

# And slug it out.
bt.fight()
victors=bt.get_actors()
print("Battle took %d turns; victors were:" % bt.get_turns())
for v in victors:
    print ("###\n%s" % str(v))
      
    
