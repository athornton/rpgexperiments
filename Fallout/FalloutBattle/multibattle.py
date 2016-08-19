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


if __name__=="__main__":
    debug=False
    quiet=True
    verbose=False
    lgr=logging.getLogger(name="Multibattle")
    lgr.setLevel(logging.DEBUG)
    ch=logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    lgr.addHandler(ch)

    trials=500
    
    catalog=load_catalog(filename="catalog.pck",debug=debug,quiet=quiet,
                         verbose=verbose,logger=lgr)

    results=dict()
    mname="Mutants (melee, ranged, overlord) vs. Deathclaw"
    results[mname]=dict()
    results[mname]["by_victor"]=dict()

    m1=catalog["creature"]["super mutant overlord"].copy()
    m1.recalc_skills()
    m1.morale=10
    m1.name="Super Mutant Overlord"
    m2=catalog["creature"]["super mutant (ranged)"].copy()
    m2.morale=9
    m2.recalc_skills()
    m2.name="Super Mutant (Ranged)"
    m3=catalog["creature"]["super mutant (melee)"].copy()
    m3.morale=9    
    m3.recalc_skills()    
    m3.name="Super Mutant (Melee)"
    
    mf=FalloutSimulator.Faction.Faction(name="mutants")
    m1.factions = [ mf ]
    m2.factions = [ mf ]
    m3.factions = [ mf ]

    d1=catalog["creature"]["deathclaw"].copy()
    d1.recalc_skills()
    d1.name="Deathclaw"
    df=FalloutSimulator.Faction.Faction(name="deathclaw")
    d1.factions=[df]
    
    mc=FalloutSimulator.Coordinates.Coordinates(x=10,y=10)
    m2.coordinates.x=11
    m2.coordinates.y=9
    m3.coordinates.x=9
    m3.coordinates.y=11

    d1.coordinates.x=40
    d1.coordinates.y=40    
    

    a1=FalloutSimulator.Arena.Arena(name=mname,
                                   quiet=quiet,debug=debug,verbose=verbose,
                                   logger=lgr)
    b1=FalloutSimulator.Battle.Battle(name=mname,arena=a1,
                                     quiet=quiet,debug=debug,
                                     verbose=verbose,logger=lgr)
    
    
    for i in range(trials):
        b=b1.copy()
        b.arena=a1.copy()
        b.add_actor_at_coords(m1.copy(),mc.copy())
        b.add_actor_at_coords(m2.copy(),mc.copy())
        b.add_actor_at_coords(m3.copy(),mc.copy())
        b.add_actor_at_coords(d1.copy(),mc.copy())

        b.fight()
        victors=b.get_actors()
        turns=b.get_turns()
        vnames=[x.name for x in victors]
        results[mname][i] = dict()
        results[mname][i]["turns"] = turns
        results[mname][i]["victors"] = vnames
        results[mname][i]["victor"]=dict()
        
        
        for vidx in range(len(vnames)):
            v=vnames[vidx]
            rmivv=None
            if not results[mname][i]["victor"].get(v):
                results[mname][i]["victor"][v] = dict()
            rmivv = results[mname][i]["victor"][v]
            rmivv["hp"]=victors[vidx].current_hp
            rmivv["max_hp"]=victors[vidx].max_hp
            if not results[mname]["by_victor"].get(v):
                results[mname]["by_victor"][v]=dict()
                results[mname]["by_victor"][v]["count"]=0
                results[mname]["by_victor"][v]["remaining_hp"]=0
                results[mname]["by_victor"][v]["total_hp"]=0
            rmbv=results[mname]["by_victor"][v]
            rmbv["total_hp"] = rmbv["total_hp"] + rmivv["max_hp"]
            rmbv["remaining_hp"] = rmbv["remaining_hp"] + rmivv["hp"]
            rmbv["count"] = rmbv["count"] + 1

    for v in results[mname]["by_victor"]:
        rmbv=results[mname]["by_victor"][v]
        ashp=(0.0 + rmbv["remaining_hp"])/rmbv["total_hp"]
        rmbv["avg_surviving_hp"]=ashp
        rmbv["avg_overall_hp"]=ashp * (rmbv["count"] + 0.0) / trials
        del(rmbv["remaining_hp"])
        del(rmbv["total_hp"])
    total_turns=0
    for i in results[mname]:
        if "turns" in results[mname][i]:
            total_turns += results[mname][i]["turns"]
    avg_turns=(total_turns + 0.0) / trials
    results[mname]["avg_turns"]=avg_turns

    print("%s: results of %d trials:" % (mname, trials))
    print(" Average battle length: %.02f turns." % results[mname]["avg_turns"])
    rmb=results[mname]["by_victor"]
    q=dict()
    for v in rmb:
        count=rmb[v]["count"]
        s = v
        s += " survived %.02f%%." % ((100*count + 0.0)/trials)
        s += " If surviving, %.02f%% HP left." % \
             (100*rmb[v]["avg_surviving_hp"])
        while count in q:
            count=count+0.01
        q[count] = s
    ll=list(q.keys())
    ls=reversed(sorted(ll))
    for tt in ls:
        print(" " + q[tt])
