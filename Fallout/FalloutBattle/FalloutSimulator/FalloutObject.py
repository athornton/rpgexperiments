#!/usr/bin/env python3
class FalloutObject(object):
    def __init__(self,*args,**kwargs):
        self.quiet=kwargs.get("quiet",False)
        self.verbose=kwargs.get("verbose",False)
        self.debug=kwargs.get("debug",False)
        self.logger=kwargs.get("logger",None)

    def __getstate__(self):
        """ This is called before pickling. """
        state = self.__dict__.copy()
        state['logger'] = None
        return state

    def __setstate__(self, state):
        """ This is called while unpickling. """
        self.__dict__.update(state)
        self.__dict__['logger']=None
        
    def log(self,msg="",*args,**kwargs):
        if not self.logger:
            return
        if self.quiet:
            return
        self.logger.info(msg,*args,**kwargs)

    def log_debug(self,msg="",*args,**kwargs):
        if not self.logger:
            return
        if not self.debug:
            return
        self.logger.debug(msg,*args,**kwargs)

    def log_warning(self,msg="",*args,**kwargs):
        if not self.logger:
            return
        if self.quiet:
            return
        self.logger.warning(msg,*args,**kwargs)

    def log_error(self,msg="",*args,**kwargs):
        if not self.logger:
            return
        if self.quiet:
            return
        self.logger.error(msg,*args,**kwargs)
