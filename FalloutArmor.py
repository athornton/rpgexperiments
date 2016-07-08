#!/usr/bin/env python3

import sys
import random
import collections
import statistics
import json
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

class FalloutArmor:
    """Armor mechanic for ignoring certain die results"""

    def __init__(self,trials=10000,jsonfile=None,outputtextfile=None,
                 outputgraphicsfile=None,
                 dicelist=None,
                 biggestdie=20,maxdice=3):
        self.trials=trials
        self.jsonfile=jsonfile
        self.outputtextfile=outputtextfile
        self.outputgraphicsfile=outputgraphicsfile
        self.dicelist=dicelist
        self.biggestdie=biggestdie
        self.maxdice=maxdice
        if jsonfile:
            self.armor=self._parse_armor_file()
        else:
            self.armor= { "No": [],
                          "Light": [4],
                          "Medium": [6],
                          "Heavy": [8],
                          "Power": [1,2,4,8,16,32,64,128] }
        if dicelist:
            dl=dicelist.split(',')
            dli=[ int(x) for x in dl ]
            self.dicelist= [ x for x in dli if x > 0 ]
        else:
            self.dicelist=[ 3,4,6,8,10,12,20,100 ]
        self.rolls=dict()

    def roll(self):
        """Roll sets of dice n=trials times and store results"""
        if self.rolls: # Throw away old set
            self.rolls=dict()
        dicelist=self.dicelist
        maxdice=self.maxdice
        biggest=self.biggestdie
        rolls=self.rolls
        dice=[ x for x in dicelist if x <= biggest ]
        for diesize in dice:
            for numdice in range(1,maxdice+1):
                dkey=str(numdice) + "d" + str(diesize)
                rolls[dkey]=dict()
                rd=rolls[dkey]
                rd["diesize"]=diesize
                rd["numdice"]=numdice
                rd["raw"]=self._rolltrials(numdice,diesize)
                rd["sum"]=[]
                for rollset in rd["raw"]:
                    rd["sum"].append(sum(rollset))

    def _rolltrials(self,numdice,diesize):
        trials=self.trials
        rollarray=[]
        for trial in range(trials):
            rollarray.append(self._rolldice(numdice,diesize))
        return rollarray

    def _rolldice(self,numdice,diesize):
        dice=[]
        for n in range(numdice):
            dice.append(random.randint(1,diesize))
        return dice

    def applyarmor(self):
        """Apply armor modifications from self.armor to rolls"""
        rolls=self.rolls
        armor=self.armor
        for dkey in rolls:
            rd=rolls[dkey]
            rd["cooked"]=dict()
            dsz=rd["diesize"]
            for key in armor:
                rd["cooked"][key]=dict()
                rdck=rd["cooked"][key]
                armorval=armor[key]
                rdck["blocks"] = armorval
                rdck["cooked"] = self._processdice(dkey,key)
                rdck=self._statify(dkey,key)

    def _processdice(self,dicekey,armorkey):
        raw=self.rolls[dicekey]["raw"]
        diesize=self.rolls[dicekey]["diesize"]
        armorval=self.armor[armorkey]
        cooked=[]
        for rollset in raw:
            cooked.append([ self._removedice(armorval,diesize,x) \
                            for x in rollset])
        return cooked

    def _removedice(self,armorvalue,diesize,x):
        if armorvalue and (max(armorvalue) > diesize) and (x == diesize):
            return 0
        if x in armorvalue:
            return 0
        return x

    def _statify(self,dicekey,armorkey):
        sumname = "sum"
        rd=self.rolls[dicekey]["cooked"][armorkey]
        rd[sumname] = []
        rdrs=rd["cooked"]
        for rollset in rdrs:
            rd[sumname].append(sum(rollset))
        rd["stddev"]=statistics.pstdev(rd[sumname])
        rd["mean"]=statistics.mean(rd[sumname])

    def report(self):
        """Output text report of rolls plus armor application"""
        f=sys.stdout
        if self.outputtextfile:
            f=open(self.outputtextfile,'w')
        trials=self.trials
        rolls=self.rolls
        armor=self.armor
        sortedrolls=collections.OrderedDict(sorted(rolls.items(), \
                                                   key=lambda t: \
                                                   1000 * (t[1])["diesize"] + \
                                                   (t[1]["numdice"])))
        for key in sortedrolls:
            dl="%-20s" % ("Damage roll: %s" % key)
            dr=dl + "(%d trials)" % trials
            f.write("%s\n" % dr)
            rk=sortedrolls[key]
            diesize=rk["diesize"]
            akeys=collections.OrderedDict(sorted(rk["cooked"].items(), \
                                                 key=lambda t: \
                                                 sum(t[1]["blocks"])))
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
                f.write("%s: mean %s; stddev %s\n" % (at2,ms,ds))
            f.write("\n")

    def _parse_armor_file(self):
        with open(self.jsonfile) as jf:
            self.armor=json.load(jf)

    def plot(self):
        """Graph distribution of rolls with armor application"""
        rolls=self.rolls
        trials=self.trials
        outputfile=self.outputgraphicsfile
        sortedrolls=collections.OrderedDict(sorted(rolls.items(), \
                                                   key=lambda t: \
                                                   1000 * (t[1])["diesize"] + \
                                                   (t[1]["numdice"])))    
        colors="kbgrcmy"
        lc=len(colors)
        pp=None
        if outputfile:
            pp=PdfPages(outputfile)
        j=1
        for tp in sortedrolls:
            i=0
            rt=sortedrolls[tp]
            fig=plt.figure(j)
            j=j+1
            plt.title("%s raw data (%d trials)" % (tp,trials))
            plt.xlabel("Damage")
            plt.ylabel("Count")
            bins=rt["numdice"] * rt["diesize"] + 1
            drange=(0,bins)
            fc=colors[i]
            i=i+1
            rawsums=rt["sum"]
            n, bins, patches = plt.hist(rawsums,bins,color=fc,range=drange)
            plt.grid(True)
            if outputfile:
                pp.savefig()
            else:
                plt.show()
            plt.close(fig)
            urolldata=rt["cooked"]
            rolldata=collections.OrderedDict(sorted(urolldata.items(), \
                                                    key=lambda t: \
                                                    sum(t[1]["blocks"])))
            for at in rolldata:
                fig=plt.figure(j)
                rat=rolldata[at]
                plt.title("%s for %s armor (%d trials)" % (tp,at,trials))
                plt.xlabel("Damage (mean=%f; std. dev.=%f)" % (rat["mean"],
                                                               rat["stddev"]))
                plt.ylabel("Count")
                sums=rat["sum"]
                fc=colors[i % lc]
                n, bins, patches = plt.hist(sums,bins,color=fc,range=drange)
                plt.grid(True)
                if outputfile:
                    pp.savefig()
                else:
                    plt.show()
                plt.close(fig)
                i=i+1
                j=j+1
        if outputfile:
            pp.close()
            
