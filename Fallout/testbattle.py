#!/usr/bin/env python3

import FalloutSimulator
import logging
import jsonpickle

def clone_and_swap_ammo(weapon,newammo):
    w=weapon.copy()
    w.ammo=newammo.copy()
    return w

def build_catalog():
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
        for i in [ 2, 3, 4, 6, 8, 10, 12, 20]:
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

    ammo["5mm"]=fam(name="5mm",damage=dmg["1d4"].copy(),
                    logger=lgr,verbose=verbose,debug=debug,quiet=quiet)
    for at in [".38","9mm",".45","10mm","20ga","5.56mm",".44","12ga",".308",
               ".50", "laser pistol","laser rifle","plasma pistol",
               "plasma rifle","grenade","nuka grenade","molotov",
               "flamer","missile","mini nuke", "bloatfly vomit",
               "mirelurk acid", "stingwing venom" ]:
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

    # Critters
    ammo["bloatfly vomit"].damage.physical=None
    ammo["bloatfly vomit"].damage.poison=d["2d4"].copy()
    ammo["mirelurk acid"].damage.physical=None
    ammo["mirelurk acid"].damage.burn=d["4d6"].copy()
    ammo["stingwing venom"].damage.physical=None
    ammo["stingwing venom"].damage.poison=d["2d6"].copy()
    
    ## Weapons
    faw=FalloutSimulator.Weapon.Weapon
    sk=FalloutSimulator.Skills.Skills
    # Melee
    weapon["punch"]=faw(name="punch",skills=sk.melee,weapontype=faw.melee,
                        damage=dmg["1d3"].copy(),
                        logger=lgr,verbose=verbose,debug=debug,quiet=quiet)
    for wn in [ "kick", "brass knuckles", "switchblade", "small knife",
                "combat knife", "machete", "baseball bat", "sledgehammer",
                "ripper", "super sledge" ]:
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

    # And some critters
    for wn in [ "radroach bite", "ghoul punch", "nail board", "mirelurk claw",
                "radscorpion sting", "mole rat bite", "stingwing sting",
                "glowing one claw", "Mr. Handy buzzsaw", "mutant hound bite",
                "mongrel bite", "mirelurk kill-claw", "radstag butt",
                "deathclaw rend" ]:
        weapon[wn]=weapon["punch"].copy()
        weapon[wn].name=wn

    weapon["radroach bite"].damage=dmg["1d2"].copy()
    weapon["radroach bite"].damage.radiation=d["1d2"].copy()
    weapon["ghoul punch"].damage=dmg["1d4"].copy()
    weapon["nail board"].damage=dmg["1d6"].copy()
    weapon["mirelurk claw"].damage=dmg["2d6"].copy()
    weapon["radscorpion sting"].damage=dmg["1d10"].copy()
    weapon["radscorpion sting"].damage.poison=d["4d8"].copy()
    weapon["mole rat bite"].damage=dmg["1d6"].copy()
    weapon["stingwing sting"].damage=dmg["1d8"].copy()
    weapon["stingwing sting"].damage.poison=d["3d8"].copy()
    weapon["glowing one claw"].damage=dmg["1d12"].copy()
    weapon["glowing one claw"].damage.radiation=d["5d4"].copy()
    weapon["Mr. Handy buzzsaw"].damage=dmg["2d8"].copy()
    weapon["mutant hound bite"].damage=dmg["1d8"].copy()
    weapon["mongrel bite"].damage=dmg["1d4"].copy()
    weapon["mongrel bite"].damage.mod=1
    weapon["mirelurk kill-claw"].damage=dmg["2d10"].copy()
    weapon["radstag butt"].damage=dmg["1d4"].copy()
    weapon["deathclaw rend"].damage=dmg["3d12"].copy()

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
                             weapontype=faw.gun,
                             w_range=rng["pistol"].copy(),
                             ammo=ammo[".38"].copy(),
                             ammo_remaining="some",
                             logger=lgr,verbose=verbose,debug=debug,
                             quiet=quiet)
    weapon[".45 pistol"]=clone_and_swap_ammo(weapon[".38 pistol"], ammo[".45"])
    weapon["10mm pistol"]=clone_and_swap_ammo(weapon[".38 pistol"],
                                              ammo["10mm"])
    for i in [ "9mm", ".45", "10mm", ".44" ]:
        weapon["%s pistol"]=clone_and_swap_ammo(weapon[".38 pistol"], ammo[i])
    weapon["laser pistol"]=clone_and_swap_ammo(weapon[".38 pistol"],
                                               ammo["laser pistol"])
    for i in ["20ga", "12ga" ]:
        weapon["%s shotgun" % i]=clone_and_swap_ammo(weapon[".38 pistol"],
                                                     ammo[i])
        weapon["%s shotgun" % i].w_range=rng["shotgun"].copy()
    weapon["combat rifle"]=clone_and_swap_ammo(weapon[".38 pistol"],
                                               ammo["5.56mm"])
    weapon["combat rifle"].w_range=rng["rifle"].copy()
    weapon["hunting rifle"]=clone_and_swap_ammo(weapon["combat rifle"],
                                                ammo[".308"])
    weapon["laser rifle"]=clone_and_swap_ammo(weapon["combat rifle"],
                                              ammo["laser rifle"])
    weapon["anti-materiel rifle"]=clone_and_swap_ammo(weapon["combat rifle"],
                                                      ammo[".50"])
    for i in ["grenade", "nuka grenade", "molotov","flamer"]:
        weapon[i]=clone_and_swap_ammo(weapon[".38 pistol"],ammo[i])
        weapon[i].w_range=rng["thrown"].copy()
        weapon[i].skill=sk.explosives
    
    weapon["flamer"].w_range=rng["flamer"].copy()
    weapon["flamer"].skill=sk.big_guns
    weapon["missile launcher"]=clone_and_swap_ammo(weapon["flamer"],
                                                   ammo["missile"])
    weapon["missile launcher"].w_range=frr(name="missile", short=10, medium=30,
                                           r_long=50,maximum=200,
                                           quiet=quiet,verbose=verbose,
                                           debug=debug,logger=lgr)
    weapon["fat man"]=clone_and_swap_ammo(weapon["flamer"],
                                          ammo["mini nuke"])
    weapon["fat man"].w_range=frr(name="mini nuke", short=15, medium=50,
                                  r_long=100,maximum=500,
                                  quiet=quiet,verbose=verbose,debug=debug,
                                  logger=lgr)

    # And some critters
    for i in [ "bloatfly vomit", "mirelurk acid", "stingwing venom" ]:
        weapon[i] = clone_and_swap_ammo(weapon[".38 pistol"],ammo[i])
    
    # Now some enemies.
    fsc=FalloutSimulator.Special.Special
    fsp=dict()
    fac=FalloutSimulator.Actor.Actor
    fst=FalloutSimulator.Strategy.Strategy
    actor=dict()
    for i in range(1,11):
        nm="s%d" % i
        actor[nm]=fac(name=nm,hp=10*i,special=fsc(s=i,p=i,e=i,c=i,i=i,a=i,l=i,
                                                  debug=debug,verbose=verbose,
                                                  quiet=quiet,logger=lgr),
                      strategy=fst(strategy=fst.melee),
                      debug=debug,verbose=verbose,quiet=quiet,logger=lgr)

    actor["radroach"]=actor["s1"].copy()
    actor["radroach"].weapons = [ weapon["radroach bite"].copy() ]
    actor["radroach"].morale = 9

    actor["junkie raider"]=actor["s2"].copy()
    actor["junkie raider"].weapons = [ weapon[".38 pistol"].copy(),
                                       weapon["switchblade"].copy() ]
    actor["junkie raider"].weapons[0].ammo_remaining="some"
    actor["junkie raider"].strategy= fst(strategy=fst.ranged)
    actor["junkie raider"].armor = armor["light"].copy()
    actor["junkie raider"].morale = 6

    actor["feral ghoul"]=actor["s3"].copy()
    actor["feral ghoul"].weapons = [ weapon["ghoul punch"].copy() ]
    actor["feral ghoul"].morale = 8

    actor["mole rat"]=actor["s4"].copy()
    actor["mole rat"].weapons = [ weapon["mole rat bite"].copy() ]
    actor["mole rat"].morale = 5

    actor["super mutant (melee)"]=actor["s5"].copy()
    actor["super mutant (melee)"].weapons = [ weapon["nail board"].copy() ]
    actor["super mutant (melee)"].armor = armor["light"].copy()
    actor["super mutant (melee)"].morale = 9

    actor["super mutant (ranged)"]=actor["s5"].copy()
    actor["super mutant (ranged)"].weapons = [ weapon["sledgehammer"].copy(),
                                               weapon["hunting rifle"].copy(),
                                               weapon["molotov"].copy()]
    actor["super mutant (ranged)"].strategy= fst(strategy=fst.ranged)
    actor["super mutant (ranged)"].weapons[1].ammo_remaining = "some"
    actor["super mutant (ranged)"].weapons[1].ammo_remaining = "some"
    actor["super mutant (ranged)"].armor = armor["light"].copy()
    actor["super mutant (ranged)"].morale = 9

    actor["raider leader"]=actor["s6"].copy()
    actor["raider leader"].weapons = [ weapon["combat knife"].copy(),
                                       weapon["combat rifle"].copy(),
                                       weapon["grenade"].copy()]
    actor["raider leader"].strategy= fst(strategy=fst.ranged)
    actor["raider leader"].weapons[1].ammo_remaining="plenty"
    actor["raider leader"].weapons[2].ammo_remaining="some"
    actor["raider leader"].morale = 9
    actor["raider leader"].armor = armor["medium"].copy()
    
    actor["raider boomer"]=actor["s6"].copy()
    actor["raider boomer"].weapons = [ weapon["combat knife"].copy(),
                                       weapon["fat man"].copy() ]
    actor["raider boomer"].strategy= fst(strategy=fst.ranged)
    actor["raider boomer"].weapons[1].ammo_remaining="3"
    actor["raider boomer"].morale = 9
    actor["raider boomer"].armor = armor["medium"].copy()

    actor["Sgt. Gutsy"]=actor["s7"].copy()
    actor["Sgt. Gutsy"].weapons = [ weapon["Mr. Handy buzzsaw"].copy(),
                                    weapon["laser rifle"].copy(),
                                    weapon["missile launcher"].copy() ]
    actor["Sgt. Gutsy"].strategy= fst(strategy=fst.ranged)
    actor["Sgt. Gutsy"].weapons[1].ammo_remaining = "plenty"
    actor["Sgt. Gutsy"].weapons[2].ammo_remaining = "some"

    actor["mirelurk killclaw"]=actor["s8"].copy()
    actor["mirelurk killclaw"].weapons = [ weapon["mirelurk kill-claw"].copy(),
                                       weapon["mirelurk acid"].copy() ]
    actor["mirelurk killclaw"].strategy = fst(strategy=fst.ranged)
    actor["mirelurk killclaw"].weapons[1].ammo_remaining="some"
    actor["mirelurk killclaw"].morale = 10
    actor["mirelurk killclaw"].armor = armor["power"].copy()
    actor["mirelurk killclaw"].armor.name = "mirelurk killclaw shell"


    actor["super mutant overlord"]=actor["s9"].copy()
    actor["super mutant overlord"].weapons = [ weapon["super sledge"].copy(),
                                               weapon["combat rifle"].copy(),
                                               weapon["nuka grenade"].copy() ]
    actor["super mutant overlord"].strategy = fst(strategy=fst.ranged)
    actor["super mutant overlord"].weapons[1].ammo_remaining="plenty"
    actor["super mutant overlord"].weapons[2].ammo_remaining="some"
    actor["super mutant overlord"].armor=armor["heavy"].copy()

    actor["deathclaw"]=actor["s10"].copy()
    actor["deathclaw"].weapons = [ weapon["deathclaw rend"].copy() ]
    actor["deathclaw"].armor = armor["heavy"].copy()
    actor["deathclaw"].armor.name = "deathclaw hide"

    catalog=dict()
    catalog["armor"]=armor
    catalog["ammo"]=ammo
    catalog["weapon"]=weapon
    catalog["creature"]=actor

    with open("catalog.jpck","w") as f:
        for k1 in catalog.keys():
            for k2 in catalog[k1].keys():
                f.write(jsonpickle.encode(catalog[k1][k2]))
                f.write("\n")
    return catalog


if __name__=="__main__":
    catalog=build_catalog()

    a=FalloutSimulator.Arena.Arena(name="Mutants vs. Deathclaw")
    b=FalloutSimulator.Battle.Battle(name="Mutants vs. Deathclaw",arena=a)

    m1=catalog["creature"]["super mutant overlord"].copy()
    m1.name="Super Mutant Overlord"
    m2=catalog["creature"]["super mutant (ranged)"].copy()
    m2.name="Super Mutant Ranged #1"
    m3=catalog["creature"]["super mutant (ranged)"].copy()
    m3.name="Super Mutant Ranged #2"
    m4=catalog["creature"]["super mutant (melee)"].copy()
    m4.name="Super Mutant Melee #1"
    m5=catalog["creature"]["super mutant (melee)"].copy()
    m5.name="Super Mutant Melee #2"
    
    mf=FalloutSimulator.Faction.Faction(name="mutants")
    m1.factions = [ mf ]
    m2.factions = [ mf ]
    m3.factions = [ mf ]
    m4.factions = [ mf ]
    m5.factions = [ mf ]    

    d1=catalog["creature"]["deathclaw"].copy()
    d1.name="Deathclaw"
    df=FalloutSimulator.Faction.Faction(name="deathclaw")
    d1.factions=[df]
    
    mc=FalloutSimulator.Coordinates.Coordinates(x=10,y=10)
    b.add_actor_at_coords(m1,mc.copy())
    b.add_actor_at_coords(m2,mc.copy())
    m2.coordinates.x=9
    m2.coordinates.y=9
    b.add_actor_at_coords(m3,mc.copy())
    m3.coordinates.x=9
    m3.coordinates.y=11
    b.add_actor_at_coords(m4,mc.copy())
    m4.coordinates.x=11
    m4.coordinates.y=11
    b.add_actor_at_coords(m5,mc.copy())
    m4.coordinates.x=11
    m4.coordinates.y=9

    b.add_actor_at_coords(d1,mc.copy())
    d1.coordinates.x=40
    d1.coordinates.y=40    

    b.fight()

    print("Victors:")
    for x in b.get_actors():
        print(x)
