#!/usr/bin/env python3

import random
import collections
import statistics
import argparse
import json

def rolltrials(trials,maxdice,biggest):
    rolls=dict()
    dicelist=[ 3,4,6,8,10,12,20,100 ]
    dice=[ x for x in dicelist if x <= biggest ]
    for diesize in dice:
        for numdice in range(1,maxdice+1):
            dkey=str(numdice) + "d" + str(diesize)
            rolls[dkey]=dict()
            rd=rolls[dkey]
            rd["diesize"]=diesize
            rd["numdice"]=numdice
            rd["raw"]=roll(trials,numdice,diesize)
    return rolls

def roll(trials,numdice,diesize):
    rollarray=[]
    for trial in range(trials):
        rollarray.append(rolldice(numdice,diesize))
    return rollarray

def rolldice(numdice,diesize):
    dice=[]
    for n in range(numdice):
        dice.append(random.randint(1,diesize))
    return dice

def processrolls(rolls,armor):
    for dkey in rolls:
        rd=rolls[dkey]
        rd["cooked"]=dict()
        dsz=rd["diesize"]
        for key in armor:
            rd["cooked"][key]=dict()
            rdck=rd["cooked"][key]
            armorval=armor[key]
            rdck["blocks"] = armorval
            rdck["cooked"] = processdice(rd["raw"],dsz,armorval)
            rdck=statify(rdck)
    return rolls

def processdice(raw,diesize,armorvalue):
    cooked=[]
    for rollset in raw:
        cooked.append([ removedice(armorvalue,diesize,x) for x in rollset])
    return cooked

def removedice(armorvalue,diesize,x):
    if armorvalue and (max(armorvalue) > diesize) and (x == diesize):
        return 0
    if x in armorvalue:
        return 0
    return x

def statify(rd):
    sumname = "sum"
    rd[sumname] = []
    rdrs=rd["cooked"]
    for rollset in rdrs:
        rd[sumname].append(sum(rollset))
    rd["stddev"]=statistics.stdev(rd[sumname])
    rd["mean"]=statistics.mean(rd[sumname])
    return rd

def reporttrials(trials,rolls,armor):
    sortedrolls=collections.OrderedDict(sorted(rolls.items(), \
                            key=lambda t: 1000 * (t[1])["diesize"] + \
                                               (t[1]["numdice"])))
    for key in sortedrolls:
        dl="%-20s" % ("Damage roll: %s" % key)
        dr=dl + "(%d trials)" % trials
        print(dr)
        rk=sortedrolls[key]
        diesize=rk["diesize"]
        akeys=collections.OrderedDict(sorted(rk["cooked"].items(), \
                                             key=lambda t: sum(t[1]["blocks"])))
        for akey in akeys:
            rka=rk["cooked"][akey]
            ak=armor[akey]
            aa=[x for x in ak if x <= diesize ]
            if ak and diesize not in aa and max(ak) > diesize:
                aa.append(diesize)
            atype="%06s armor" % akey
            if armor[akey]:
                at2="%-45s" % ("%s (blocks %s)" % (atype,aa))
            else:
                at2="%-45s" % atype
            ms="%8s" % ("%02.5f" % rka["mean"])
            ds="%8s" % ("%02.5f" % rka["stddev"])
            print("%s: mean %s; stddev %s" % (at2,ms,ds))
        print("")

def parse_armor_file(filename):
    with open(filename) as jf:
        data=json.load(jf)
    return data

def parse_my_args():
    parser = argparse.ArgumentParser(description=
                                     'Get damage reduction statistics.')
    parser.add_argument("-t","--trials",type=int,default=10000,
                        help="# of trials to run")
    parser.add_argument("-j","--jsonfile",
                        help="JSON file containing armor definitions")
    parser.add_argument("-m","--maxdice",type=int, default=6,
                        help="Maximum number of dice to roll.")
    parser.add_argument("-b","--biggest",type=int, default=20,
                        help="Biggest die (from standard D&D set of " +\
                        "[ 3, 4, 6, 8, 10, 12, 20, 100 ] to roll.")
    args = parser.parse_args()
    return args

def main():
    args=parse_my_args()
    armor=dict()
    if args.jsonfile:
        armor=parse_armor_file(args.jsonfile)
    else:
        armor= { "No": [],
                 "Light": [4],
                 "Medium": [6],
                 "Heavy": [8],
                 "Power": [1,2,4,8,16,32,64,128] }
    trials=args.trials
    rawrolls=rolltrials(trials,args.maxdice,args.biggest)
    rolls=processrolls(rawrolls,armor)
    reporttrials(trials,rolls,armor)

if __name__ == "__main__":
    main()
    
