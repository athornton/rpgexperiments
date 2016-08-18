#!/usr/bin/env python3

import FalloutSimulator
import logging
import pickle

def clone_and_swap_ammo(weapon,newammo):
    w=weapon.copy()
    w.ammo=newammo.copy()
    w.damage=w.ammo.damage
    return w

def load_catalog(filename=None,debug=False,quiet=False,verbose=False,
                 logger=None):
    with open(filename,"rb") as f:
        catalog = pickle.load(f)
    for k in catalog:
        for kk in catalog[k]:
            catalog[k][kk].debug=debug
            catalog[k][kk].quiet=quiet
            catalog[k][kk].verbose=verbose
            catalog[k][kk].logger=logger
    return catalog


if __name__=="__main__":
    debug=False
    quiet=True
    verbose=False
    name="Raider vs. Raider"
    lgr=logging.getLogger(name=name)
    lgr.setLevel(logging.DEBUG)
    ch=logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    lgr.addHandler(ch)
    
    catalog=load_catalog(filename="catalog.pck",debug=debug,quiet=quiet,
                         verbose=verbose,logger=lgr)

    
    a=FalloutSimulator.Arena.Arena(name=name,
                                   quiet=quiet,debug=debug,verbose=verbose,
                                   logger=lgr)
    b=FalloutSimulator.Battle.Battle(name=name,arena=a,
                                     quiet=quiet,debug=debug,verbose=verbose,
                                     logger=lgr)

    r1=catalog["creature"]["junkie raider"].copy()
    r1.morale=8
    r1.recalc_skills()
    r1.name="Raider Junkie #1"
    r2=catalog["creature"]["junkie raider"].copy()
    r2.morale=8    
    r2.recalc_skills()
    r2.name="Raider Junkie #2"
    r1f=FalloutSimulator.Faction.Faction(name="Raider #1")
    r1.factions = [ r1f ]
    r2f=FalloutSimulator.Faction.Faction(name="Raider #2")    
    r2.factions = [ r2f ]
    rc=FalloutSimulator.Coordinates.Coordinates(x=10,y=10)
    b.add_actor_at_coords(r1,rc.copy())
    b.add_actor_at_coords(r2,rc.copy())
    r2.coordinates.x=40
    r2.coordinates.y=40
    victors=b.fight()
    print("Victors (%d turns):" % b.get_turns())
    for x in victors:
        print(x)
