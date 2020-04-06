from AccS_module import *
from AccS_restserver_module import restserver_module
import json

class AccS:
    def __init__(self) :
        self.dataDic = {
            "pH" : "UNINITIALIZED",
            "o2" : "UNINITIALIZED",
            "co2" : "UNINITIALIZED",
            "EC" : "UNINITIALIZED",
            "ebo" : "UNINITIALIZED"
        }
        self.loadedModules = []
        
    def loadModule(self, module) :
        self.loadedModules.append(module)
        print("loading module %s" % module.name)
        module.onStart()
    
    def printMods(self) :
        for m in self.loadedModules :
            print(m.name)
            
            
    def printDataDic (self) :
        for d in self.dataDic :
            print (d, self.dataDic[d])
            
        print("--------------------------------")
            
    def mainLoop(self) :
        while True :
            try :
                for m in self.loadedModules :
                    m.onUpdate()        
                #print(self.dataDic)
                #self.printDataDic()
                    
            #attempt to gracefully stop the program 
            except KeyboardInterrupt :
                print("stopping because keyboard interrupt")
                for m in self.loadedModules :
                    m.onStop()
                return            
            except Exception as e:
                print("stopping because exception")
                for m in self.loadedModules :
                    m.onStop()
                raise e
                
            
AccS_Main_Controller = AccS()
AccS_Main_Controller.printMods()
#mod = module(AccS_Main_Controller,"tryVictory")
mod = inputModule(AccS_Main_Controller)
restserver = restserver_module(AccS_Main_Controller)
AccS_Main_Controller.loadModule(mod)
AccS_Main_Controller.loadModule(restserver)
#print(json.dumps(AccS_Main_Controller.dataDic,indent=0))
AccS_Main_Controller.mainLoop()