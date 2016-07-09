#!/usr/bin/env python3
import argparse
import FalloutArmor

def _parse_my_args():
    parser = argparse.ArgumentParser(description=
                                     'Get damage reduction statistics')
    parser.add_argument("-t","--trials",type=int,default=10000,
                        help="# of trials to run [10000]")
    parser.add_argument("-j","--jsonfile",
                        help="JSON file containing armor definitions " + \
                        "[ { 'No': [], 'Light': [4], 'Medium': [6], " + \
                        "'Heavy': [8], 'Power': [1,2,4,8,16,32,64,128] } ]")
    parser.add_argument("-m","--maxdice",type=int, default=6,
                        help="Maximum number of dice to roll [6]")
    parser.add_argument("-d","--diceset",
                        help="Comma-separated list of die sizes to check" + \
                        " [ 3,4,6,8,10,12,20,100 ]")
    parser.add_argument("-b","--biggest",type=int, default=20,
                        help="Biggest die from diceset to roll [20]")
    parser.add_argument("-g","--graphicaloutput",help="Plot output file" + \
                         " ('' disables) [displayed]")
    parser.add_argument("-o","--output",help="Text output file" + \
                        " [stdout]")
    args = parser.parse_args()
    return args
    
def main():
    args=_parse_my_args()
    armorobj=FalloutArmor.FalloutArmor(trials=args.trials,
                                       jsonfile=args.jsonfile,
                                       dicelist=args.diceset,
                                       maxdice=args.maxdice,
                                       biggestdie=args.biggest,
                                       outputgraphicsfile=args.graphicaloutput,
                                       outputtextfile=args.output)
    armorobj.roll()
    armorobj.applyarmor()
    armorobj.report()
    if args.graphicaloutput == None or args.graphicaloutput != '':
        armorobj.plot()

if __name__ == "__main__":
    main()
