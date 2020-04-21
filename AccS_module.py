#base class for modules
class AccS_module(object):
    def __init__(self, accS, name) :
        self.accS = accS
        self.name = name
        
    #function to be run on load
    def onStart (self) :
        pass
       
    #function to be called every iteration
    def onUpdate (self) :
        pass
    
    #function to be called to gracefully stop the module. (closing files, stopping processes, etc.)
    def onStop (self) :
        print("stopping %s" % self.name) 

