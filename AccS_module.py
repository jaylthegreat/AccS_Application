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
    
    def onStop (self) :
        print("stopping %s" % self.name) 

import serial, string
import datetime

class inputModule(AccS_module) :
    def __init__(self,accS):
        super(inputModule, self).__init__(accS, "sensor_input_handler")
        
        
    def onStart (self) :
        print("opening serial connection ... ")
        self.count = 0
        #self.input_log = open("../data/log.txt", "w")
        #should prolly add some error handling here later
        self.ser = serial.Serial('/dev/ttyACM0', 9600, 8, 'N', 1 ,timeout=5)
        self.input = " "
    
    def onUpdate(self) :
        if self.input != "" and self.input != "\n" and self.input:
            #print (self.count, str(self.output))
            self.count += 1
            #self.f.write(str(self.output))
            data = self.ser.readline().decode().strip('\n')
            self.input = data
            self.processEZOInputLine(data)
            
    def processEZOInputLine (self, data) :
        if len(data.strip(' ')) == 0 or data == "" or data == " " or data[0] == ' ':
            return
        line = data.split(' ')
        #self.accS.dataDic[line[0]] = datetime.datetime.now().strftime("%Y_%m%d_%H_%M_%s") + " " + data[len(line[0]):-1]
        self.accS.dataDic[line[0]] = data[len(line[0]):-1]
