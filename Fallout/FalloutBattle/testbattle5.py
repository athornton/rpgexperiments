#!/usr/bin/env python3

import FalloutSimulator
import logging
import pickle
import argparse
import random

def _parse_my_args():
    parser = argparse.ArgumentParser(description='Run a battle')
    parser.add_argument("-d","--debug",action='store_true',
                        help="enable debug logging")
    parser.add_argument("-v","--verbose",action='store_true',
                        help="verbose object descriptions")
    parser.add_argument("-q","--quiet",action='store_true',
                        help="suppress battle logs")
    parser.add_argument("-c","--catalog",default="./catalog.pck",
                        help="pickle file containing object catalog")
    parser.add_argument("-o","--output",help="Text output file [stdout]")
    parser.add_argument("-s","--silent",action='store_true',
                        help="Omit all text output")
    args = parser.parse_args()
    return args

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
    for k in catalog["ammo"]:
        dd=catalog["ammo"][k].damage
        dd.debug=debug
        dd.quiet=quiet
        dd.verbose=verbose
        dd.logger=logger
        for dt in [ dd.physical, dd.burn, dd.radiation, dd.poison ]:
            if dt:
                dt.debug=debug
                dt.quiet=quiet
                dt.verbose=verbose
                dt.logger=logger
                for dx in dt.dice:
                    dx.debug=debug
                    dx.quiet=quiet
                    dx.verbose=verbose
                    dx.logger=logger
    return catalog


def main():
    args = _parse_my_args()
    debug=args.debug
    quiet=args.quiet
    silent=args.silent
    verbose=args.verbose
    bname="Ghouls vs. Mole Rats"
    lgr=logging.getLogger(name=bname)
    lgr.setLevel(logging.DEBUG)
    ch=logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    lgr.addHandler(ch)
    if args.output:
        fh=logging.FileHandler(args.output)
        fh.setLevel(logging.DEBUG)
        lgr.addHandler(fh)
    cfile=args.catalog
    
    catalog=load_catalog(filename=cfile,debug=debug,quiet=quiet,
                         verbose=verbose,logger=lgr)
    
    
    ar=FalloutSimulator.Arena.Arena(name=bname,
                                    quiet=quiet,debug=debug,verbose=verbose,
                                    logger=lgr)
    b=FalloutSimulator.Battle.Battle(name=bname,arena=ar,
                                     quiet=quiet,debug=debug,verbose=verbose,
                                     logger=lgr)


    r1=catalog["creature"]["feral ghoul"].copy()
    r1.name="Feral Ghoul #1"
    r2=catalog["creature"]["feral ghoul"].copy()
    r2.name="Feral Ghoul #2"
    r3=catalog["creature"]["feral ghoul"].copy()
    r3.name="Feral Ghoul #3"
    r4=catalog["creature"]["feral ghoul"].copy()
    r4.name="Feral Ghoul #4"
    r5=catalog["creature"]["feral ghoul"].copy()
    r5.name="Feral Ghoul #5"
    r6=catalog["creature"]["glowing one"].copy()
    r6.name="Glowing One"
    r1f=FalloutSimulator.Faction.Faction(name="Ghouls")
    r1.factions = [ r1f ]
    r2.factions = [ r1f ]
    r3.factions = [ r1f ]
    r4.factions = [ r1f ]
    r5.factions = [ r1f ]
    r6.factions = [ r1f ]

    
    m1=catalog["creature"]["mole rat"].copy()
    m1.name="Mole Rat #1"
    m2=catalog["creature"]["mole rat"].copy()
    m2.name="Mole Rat #2"
    m3=catalog["creature"]["mole rat"].copy()
    m3.name="Mole Rat #3"
    m4=catalog["creature"]["mole rat"].copy()
    m4.name="Mole Rat #4"
    m5=catalog["creature"]["mole rat"].copy()
    m5.name="Mole Rat #5"
    m6=catalog["creature"]["mole rat"].copy()
    m6.name="Mole Rat #6"
    m7=catalog["creature"]["mole rat brood mother"].copy()
    m7.name="Mole Rat Brood Mother"
    mf=FalloutSimulator.Faction.Faction(name="Mole Rats")    
    m1.factions = [ mf ]
    m2.factions = [ mf ]
    m3.factions = [ mf ]
    m4.factions = [ mf ]
    m5.factions = [ mf ]
    m6.factions = [ mf ]
    m7.factions = [ mf ]    
    
    rc=FalloutSimulator.Coordinates.Coordinates(x=10,y=10)
    b.add_actor_at_coords(r1,rc.copy())
    b.add_actor_at_coords(r2,rc.copy())
    b.add_actor_at_coords(r3,rc.copy())
    b.add_actor_at_coords(r4,rc.copy())
    b.add_actor_at_coords(r5,rc.copy())
    b.add_actor_at_coords(r6,rc.copy())
    for a in [ r1, r2, r3, r4, r5, r6 ]:
        a.coordinates.x = random.randint(1,5) + 7
        a.coordinates.y = random.randint(1,5) + 7
    b.add_actor_at_coords(m1,rc.copy())
    b.add_actor_at_coords(m2,rc.copy())
    b.add_actor_at_coords(m3,rc.copy())
    b.add_actor_at_coords(m4,rc.copy())
    b.add_actor_at_coords(m5,rc.copy())
    b.add_actor_at_coords(m6,rc.copy())
    b.add_actor_at_coords(m7,rc.copy())
    for a in [ m1, m2, m3, m4, m5, m6 ]:
        a.coordinates.x = random.randint(1,5) + 37
        a.coordinates.y = random.randint(1,5) + 37
    victors=b.fight()
    lfn=lgr.info
    if silent and quiet:
        pass
    else:
        if quiet:
            lfn=print
        lfn("Victors (%d turns):" % b.get_turns())
        for x in victors:
            lfn(x)
        
if __name__=="__main__":
    main()

