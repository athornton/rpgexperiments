#!/usr/bin/env python3

from .FalloutException import FalloutException
class DiceException(FalloutException):
    def __init__(self,*args,**kwargs):
        FalloutException.__init__(self,*args,**kwargs)
    
