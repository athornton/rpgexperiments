#!/usr/bin/env python3

import FalloutSimulator
import logging
import pickle
import argparse

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
    bname="Raider vs. Raider"
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
    
    
    a=FalloutSimulator.Arena.Arena(name=bname,
                                   quiet=quiet,debug=debug,verbose=verbose,
                                   logger=lgr)
    b=FalloutSimulator.Battle.Battle(name=bname,arena=a,
                                     quiet=quiet,debug=debug,verbose=verbose,
                                     logger=lgr)


    r1=catalog["creature"]["raider leader"].copy()
    r1.recalc_skills()
    r1.name="Raider Leader"
    r2=catalog["creature"]["stingwing"].copy()
    r2.recalc_skills()
    r2.name="Stingwing"
    r1f=FalloutSimulator.Faction.Faction(name="Raider Leader")
    r1.factions = [ r1f ]
    r2f=FalloutSimulator.Faction.Faction(name="Stingwing")    
    r2.factions = [ r2f ]
    rc=FalloutSimulator.Coordinates.Coordinates(x=10,y=10)
    b.add_actor_at_coords(r1,rc.copy())
    b.add_actor_at_coords(r2,rc.copy())
    r2.coordinates.x=40
    r2.coordinates.y=40

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

