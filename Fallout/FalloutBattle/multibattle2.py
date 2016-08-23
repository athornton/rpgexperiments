#!/usr/bin/env python3

import FalloutSimulator
import logging
import pickle
import argparse

def _parse_my_args():
    parser = argparse.ArgumentParser(description=
                                     'Run multiple trials of battle')
    parser.add_argument("-t","--trials",type=int,default=300,
                        help="# of trials to run [300]")
    parser.add_argument("-d","--debug",action='store_true',
                        help="enable debug logging")
    parser.add_argument("-v","--verbose",action='store_true',
                        help="verbose object descriptions")
    parser.add_argument("-q","--quiet",default=True,
                        action='store_true',help="suppress battle logs")
    parser.add_argument("-c","--catalog",default="./catalog.pck",
                        help="pickle file containing object catalog")
    parser.add_argument("-o","--output",help="Text output file [stdout]")
    parser.add_argument("-g","--graphicaloutput",help="Plot output file" +
                        "[None]")
    parser.add_argument("-n","--noplot",default=False,action='store_true',
                        help="Omit graphical output to screen")
    parser.add_argument("-s","--silent",action='store_true',default=False,
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

def plot(results,enemylist,trials,outputfile,noplot):
    if not outputfile and noplot:
        return
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
                if e != "Mirelurk Killclaw":
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
        colors=["Red", "Green" ]
        for i in range(0,2):
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
        plt.ylabel('HP remaining (Mirelurk shown as negative)')
            
        plt.title("Survival of %s" % mn)
        plt.legend(p,enemylist,loc=2)
        if outputfile:
            plt.savefig(outputfile,format="pdf")
        if not noplot:
            plt.show()

def main():
    args = _parse_my_args()
    debug=args.debug
    quiet=args.quiet
    silent=args.silent
    verbose=args.verbose
    lgr=logging.getLogger(name="Multibattle")
    lgr.setLevel(logging.DEBUG)
    ch=logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    lgr.addHandler(ch)
    if args.output:
        fh=logging.FileHandler(args.output)
        fh.setLevel(logging.DEBUG)
        lgr.addHandler(fh)
    trials=args.trials
    cfile=args.catalog
    
    catalog=load_catalog(filename=cfile,debug=debug,quiet=quiet,
                         verbose=verbose,logger=lgr)
    noplot=args.noplot
    gfile=args.graphicaloutput
    
    results=dict()
    mname="Sgt. Gutsy vs. Mirelurk Killclaw"
    results[mname]=dict()
    results[mname]["by_victor"]=dict()

    enemylist=[ "Sgt. Gutsy", "Mirelurk Killclaw" ]

    r1=catalog["creature"]["Sgt. Gutsy"].copy()
    r1.recalc_skills()
    r1.name=enemylist[0]

    r1f=FalloutSimulator.Faction.Faction(name="Sgt. Gutsy")
    r1.factions = [ r1f ]

    d1=catalog["creature"]["mirelurk killclaw"].copy()
    d1.recalc_skills()
    d1.name=enemylist[1]
    df=FalloutSimulator.Faction.Faction(name="mirelurk killclaw")
    d1.factions=[df]

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
        b.add_actor_at_coords(r1.copy(),r1.coordinates.copy())
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

    s1 = "%s: results of %d trials:" % (mname, trials)
    s2 = " Average battle length: %.02f turns." % results[mname]["avg_turns"]
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
    rr = []
    ll=list(q.keys())
    ls=reversed(sorted(ll))
    for tt in ls:
        rr.append(" " + q[tt])
    lfn=lgr.info
    if quiet and silent:
        pass
    else:
        if quiet:
            lfn=print
        lfn(s1)
        lfn(s2)
        for rrr in rr:
            lfn(rrr)
                
    plot(results,enemylist,trials,gfile,noplot)
       
if __name__=="__main__":
    main()

