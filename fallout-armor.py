#!/usr/bin/env python3
import argparse
import FalloutArmor

def _parse_my_args():
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
    parser.add_argument("-g","--graphicaloutput",help="Output file for plots")
    parser.add_argument("-o","--output",help="Output text file for report")
    args = parser.parse_args()
    return args
    
def main():
    args=_parse_my_args()
    armorobj=FalloutArmor.FalloutArmor(trials=args.trials,
                                       jsonfile=args.jsonfile,
                                       maxdice=args.maxdice,
                                       biggestdie=args.biggest,
                                       outputgraphicsfile=args.graphicaloutput,
                                       outputtextfile=args.output)
    armorobj.roll()
    armorobj.applyarmor()
    armorobj.report()
    armorobj.plot()

if __name__ == "__main__":
    main()
