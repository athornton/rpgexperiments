#!/usr/bin/env python3

from .FalloutObject import FalloutObject
class Strategy(FalloutObject):
    melee="melee"
    ranged="ranged"
    flee="flee"
    nothing="nothing"

    def __init__(self,strategy,**kwargs):
        super(Strategy,self).__init__(**kwargs)
        if strategy == Strategy.melee or strategy == Strategy.ranged or \
           strategy == Strategy.flee or strategy == Strategy.nothing:
            self.strategy=strategy
        else:
            raise StrategyException("Unknown strategy %s" % strategy)

    def __str__(self):
        return self.strategy

    def copy(self):
        s = Strategy(strategy=self.strategy,debug=self.debug,
                     verbose=self.verbose,quiet=self.quiet,logger=self.logger)
        return s

                    
    
