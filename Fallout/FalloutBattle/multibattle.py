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

def plot(results,enemylist,trials):
    import numpy as np
    import matplotlib.pyplot as plt
    
    for mn in results:
        allnames=list((results[mn]["by_victor"]).keys())
        hp=dict()
        for n in allnames:
            hp[n]=[]
        for i in results[mn]:
            if i in [ "by_victor", "avg_turns" ]:
                continue
            v=results[mn][i]["victor"]
            idig=int(i)
            vs=list(v.keys())
            for n in allnames:
                if n not in vs:
                    hp[n].append(0)
                else:
                    a=v[n]
                    pct=a["hp"]
                    hp[n].append(pct)
        hs = []
        for e in enemylist:
            if e in hp:
                if e != "Deathclaw":
                    hs.append(hp[e])
                else:
                    hs.append([ -x for x in hp[e] ])
            else:
                hs.append([0] * trials)
        rt=range(trials)
        sorttuple=[]
        for i in rt:
            xsum=0
            for j in range(len(hs)):
                tl = hs[j]
                xsum = xsum + tl[i]
            sorttuple.append( (xsum,i) )
        sstuple = sorted(sorttuple)
        sortlist = [ x[1] for x in sstuple ] 
        ss = []
        for i in range(len(hs)):
            sl = []
            for so in sortlist:
                tl = hs[i]
                sl.append(tl[so])
            ss.append(sl)
        w=1
        p=[]
        colors=["Red", "DarkRed", "Gold", "Salmon", "Green" ]
        for i in range(0,5):
            if i == 0 or i == (len(colors) - 1):
                b=[0]*trials
            else:
                b=[]
                for j in range(trials):
                    sumb = 0
                    for k in range(i):
                      sumb = sumb + ss[k][j]
                    b.append(sumb)
            p.append(plt.bar(rt,ss[i],w,color=colors[i],bottom=b,
                             edgecolor="none"))
        plt.ylabel('HP remaining (Deathclaw shown as negative)')
            
        plt.title("Survival of %s" % mname)
        plt.legend(p,enemylist,loc=2)
        plt.savefig("MutantsVsDeathclaw.pdf",format="pdf")
        plt.show()

if __name__=="__main__":
    debug=False
    quiet=True
    verbose=False
    lgr=logging.getLogger(name="Multibattle")
    lgr.setLevel(logging.DEBUG)
    ch=logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    lgr.addHandler(ch)

    trials=300

    
    catalog=load_catalog(filename="catalog.pck",debug=debug,quiet=quiet,
                         verbose=verbose,logger=lgr)

    results=dict()
    mname="Mutants (melee x 2, ranged, overlord) vs. Deathclaw"
    results[mname]=dict()
    results[mname]["by_victor"]=dict()

    enemylist=[ "Super Mutant Overlord", "Super Mutant (Ranged)",
                "Super Mutant (Melee) #1","Super Mutant (Melee) #2",
                "Deathclaw" ]

    
    m1=catalog["creature"]["super mutant overlord"].copy()
    m1.recalc_skills()
    m1.morale=10
    m1.name=enemylist[0]
    m2=catalog["creature"]["super mutant (ranged)"].copy()
    m2.morale=9
    m2.recalc_skills()
    m2.name=enemylist[1]
    m3=catalog["creature"]["super mutant (melee)"].copy()
    m3.morale=9    
    m3.recalc_skills()    
    m3.name=enemylist[2]
    m4=catalog["creature"]["super mutant (melee)"].copy()
    m4.morale=9    
    m4.recalc_skills()    
    m4.name=enemylist[3]
    
    mf=FalloutSimulator.Faction.Faction(name="mutants")
    m1.factions = [ mf ]
    m2.factions = [ mf ]
    m3.factions = [ mf ]
    m4.factions = [ mf ]

    d1=catalog["creature"]["deathclaw"].copy()
    d1.recalc_skills()
    d1.name=enemylist[4]
    df=FalloutSimulator.Faction.Faction(name="deathclaw")
    d1.factions=[df]
    
    mc=FalloutSimulator.Coordinates.Coordinates(x=10,y=10)
    m2.coordinates.x=9
    m2.coordinates.y=9
    m3.coordinates.x=9
    m3.coordinates.y=11
    m4.coordinates.x=11
    m4.coordinates.y=9
    
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
        b.add_actor_at_coords(m1.copy(),m1.coordinates.copy())
        b.add_actor_at_coords(m2.copy(),m2.coordinates.copy())
        b.add_actor_at_coords(m3.copy(),m3.coordinates.copy())
        b.add_actor_at_coords(m4.copy(),m4.coordinates.copy())
        b.add_actor_at_coords(d1.copy(),d1.coordinates.copy())

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
    
    plot(results,enemylist,trials)
        

