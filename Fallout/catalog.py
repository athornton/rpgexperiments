#!/usr/bin/env python3

import FalloutSimulator
import logging
import jsonpickle

def clone_and_swap_ammo(weapon,newammo):
    w=weapon.copy()
    w.ammo=newammo.copy()
    return w

debug=False
verbose=False
quiet=False

lgr=logging.getLogger(name="Catalog")
lgr.setLevel(logging.DEBUG)
ch=logging.StreamHandler()
ch.setLevel(logging.DEBUG)
lgr.addHandler(ch)

armor=dict()
ammo=dict()
weapon=dict()
creature=dict()
d=dict()
dmg=dict()

# Set of dice and physical damages
dc=FalloutSimulator.Dice.Dice
dmm=FalloutSimulator.Damage.Damage

for j in range(1,7):
    for i in [ 3, 4, 6, 8, 10, 12, 20]:
        k="%dd%d" % (j,i)
        d[k]=dc(num_dice=j,sides=i,
                logger=lgr,verbose=verbose,debug=debug,quiet=quiet)
        dmg[k]=dmm(physical=d[k].copy(),
                logger=lgr,verbose=verbose,debug=debug,quiet=quiet)

faa=FalloutSimulator.Armor.Armor
am = { "light": faa.light,
       "medium": faa.medium,
       "heavy": faa.heavy,
       "power": faa.power }
for at in am.keys():
    armor[at] = faa(name='%s armor' % at,
                     armortype=am[at],
                     logger=lgr,verbose=verbose,debug=debug,quiet=quiet)

fam=FalloutSimulator.Ammo.Ammo
# Small guns
ammo["5mm"]=fam(name="5mm",damage=dmg["1d4"].copy(),
                logger=lgr,verbose=verbose,debug=debug,quiet=quiet)
for at in [".38","9mm",".45","10mm","20ga","5.56mm",".44","12ga",".308",".50",
           "laser pistol","laser rifle","plasma pistol","plasma rifle",
           "grenade","nuka grenade","molotov",
           "flamer","missile","mini nuke"]:
    ammo[at]=ammo["5mm"].copy()
    ammo[at].name=at
ammo[".38"].damage=dmg["1d6"].copy()
ammo["9mm"].damage=dmg["1d6"].copy()
ammo[".45"].damage=dmg["1d8"].copy()
ammo["10mm"].damage=dmg["1d8"].copy()
ammo["20ga"].damage=dmg["2d4"].copy()
ammo["5.56mm"].damage=dmg["1d10"].copy()
ammo[".44"].damage=dmg["1d10"].copy()
ammo["12ga"].damage=dmg["3d4"].copy()
ammo[".308"].damage=dmg["2d6"].copy()
ammo[".50"].damage=dmg["2d10"].copy()

# Energy
ammo["laser pistol"].damage=dmg["1d6"].copy()
ammo["laser rifle"].damage=dmg["1d10"].copy()
ammo["plasma pistol"].damage=dmg["3d4"].copy()
ammo["plasma pistol"].damage.radiation=d["1d4"].copy()
ammo["plasma rifle"].damage=dmg["2d8"].copy()
ammo["plasma rifle"].damage.radiation=d["1d6"].copy()

# Thrown
ammo["grenade"].damage=dmg["3d6"].copy()
ammo["grenade"].splash_radius=2
ammo["nuka grenade"].damage=dmg["4d8"].copy()
ammo["nuka grenade"].splash_radius=3
ammo["nuka grenade"].damage.radiation=d["1d6"].copy()
ammo["molotov"].damage.physical=None
ammo["molotov"].damage.burn=d["6d4"].copy()
ammo["molotov"].splash_radius=1

# Heavy
ammo["flamer"].damage.physical=None
ammo["flamer"].damage.burn=d["4d4"].copy()
ammo["missile"].damage=dmg["5d6"].copy()
ammo["missile"].splash_radius=2
ammo["mini nuke"].damage=dmg["6d20"].copy()
ammo["mini nuke"].damage.radiation=d["4d12"].copy()
ammo["mini nuke"].splash_radius=5

## Weapons
faw=FalloutSimulator.Weapon.Weapon
sk=FalloutSimulator.Skills.Skills
# Melee
weapon["punch"]=faw(name="punch",skills=sk.melee,weapontype=faw.melee,
                    damage=dmg["1d3"].copy(),
                    logger=lgr,verbose=verbose,debug=debug,quiet=quiet)
for wn in [ "kick", "brass knuckles", "switchblade", "small knife",
            "combat knife", "machete", "baseball bat", "sledgehammer",
            "ripper", "super sledge"]:
    weapon[wn]=weapon["punch"].copy()
    weapon[wn].name=wn
    
weapon["brass knuckles"].damage.physical.mod = 1
weapon["switchblade"].damage=dmg["1d4"].copy()
weapon["small knife"].damage=dmg["1d4"].copy()
weapon["combat knife"].damage=dmg["1d6"].copy()
weapon["machete"].damage=dmg["1d6"].copy()
weapon["baseball bat"].damage=dmg["1d6"].copy()
weapon["sledgehammer"].damage=dmg["1d6"].copy()
weapon["ripper"].damage=dmg["1d10"].copy()
weapon["super sledge"].damage=dmg["1d10"].copy()

#Ranged
# Make some ranges:
rng=dict()
frr=FalloutSimulator.Range.Range
                  
rm= { "pistol": [ 10, 25, 50, 100 ],
      "rifle": [ 20, 50, 100, 400 ],
      "shotgun": [ 5, 10, 20, 25 ],
      "flamer": [ 3, 5, 10, 15 ],
      "thrown": [ 5, 10, 25, 26 ], }

for r in rm.keys():
    rng[r]=frr(name=r, short=rm[r][0], medium=rm[r][1], r_log=rm[r][2],
               maximum = rm[r][3],quiet=quiet,verbose=verbose,debug=debug,
               logger=lgr)

weapon[".38 pistol"]=faw(name=".38 pistol",skills=sk.small_guns,
                         weapontype=faw.gun,w_range=rng["pistol"].copy(),
                         ammo=ammo[".38"].copy(),
                         ammo_remaining="some",
                         logger=lgr,verbose=verbose,debug=debug,quiet=quiet)
weapon[".45 pistol"]=clone_and_swap_ammo(weapon[".38 pistol"], ammo[".45"])
weapon["10mm pistol"]=clone_and_swap_ammo(weapon[".38 pistol"], ammo["10mm"])
for i in [ "9mm", ".45", "10mm", ".44" ]:
    weapon["%s pistol"]=clone_and_swap_ammo(weapon[".38 pistol"], ammo[i])
for i in ["20ga", "12ga" ]:
    weapon["%s shotgun" % i]=clone_and_swap_ammo(weapon[".38 pistol"], ammo[i])
    weapon["%s shotgun" % i].w_range=rng["shotgun"].copy()
weapon["combat rifle"]=clone_and_swap_ammo(weapon[".38 pistol"],
                                           ammo["5.56mm"])
weapon["combat rifle"].w_range=rng["rifle"].copy()
weapon["hunting rifle"]=clone_and_swap_ammo(weapon["combat rifle"],
                                            ammo[".308"])
weapon["anti-materiel rifle"]=clone_and_swap_ammo(weapon["combat rifle"],
                                                  ammo[".50"])
for i in ["grenade", "nuka grenade", "molotov","flamer"]:
    weapon[i]=clone_and_swap_ammo(weapon[".38 pistol"],ammo[i])
    weapon[i].w_range=rng["thrown"].copy()
weapon["flamer"].w_range=rng["flamer"].copy()
weapon["missile launcher"]=clone_and_swap_ammo(weapon[".38 pistol"],
                                               ammo["missile"])
weapon["missile launcher"].w_range=frr(name="missile", short=10, medium=30,
                                       r_long=50,maximum=200,
                                       quiet=quiet,verbose=verbose,debug=debug,
                                       logger=lgr)
weapon["fat man"]=clone_and_swap_ammo(weapon[".38 pistol"],
                                      ammo["mini nuke"])
weapon["fat man"].w_range=frr(name="mini nuke", short=15, medium=50,
                              r_long=100,maximum=500,
                                       quiet=quiet,verbose=verbose,debug=debug,
                                       logger=lgr)

catalog=dict()
catalog["armor"]=armor
catalog["ammo"]=ammo
catalog["weapon"]=weapon

with open("catalog.jpck","w") as f:
    for k1 in catalog.keys():
        for k2 in catalog[k1].keys():
            f.write(jsonpickle.encode(catalog[k1][k2]))
            f.write("\n")


