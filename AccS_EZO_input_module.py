#!/usr/bin/env python
from AccS_module import AccS_module

########### Separate EZOinput_module into another file another file
import serial, string
import datetime

class EZOinput_module(AccS_module) :
    def __init__(self,accS):
        super(EZOinput_module, self).__init__(accS, "sensor_input_handler")
        
        
    def onStart (self) :
        print("opening serial connection ... ")
        self.count = 0
        #self.input_log = open("../data/log.txt", "w")
        #should prolly add some error handling here later
        self.ser = serial.Serial('/dev/ttyACM0', 9600, 8, 'N', 1 ,timeout=5)
        self.input = " "
    
    def onUpdate(self) :
        if self.input != "" and self.input != "\n" and self.input:

            self.count += 1

            data = self.ser.readline().decode().strip('\n')
            self.input = data
            self.processEZOInputLine(data)
            
    def processEZOInputLine (self, data) :
        #ignore empty lines or lines that start with space.
        #this is early level of filtering the input. eventually the system will need to be revamped so that it does not use bad inputs
        if len(data.strip(' ')) == 0 or data == "" or data == " " or data[0] == ' ':
            return
        line = data.split(' ')
        #self.accS.dataDic[line[0]] = datetime.datetime.now().strftime("%Y_%m%d_%H_%M_%s") + " " + data[len(line[0]):-1]
        self.accS.dataDic[line[0]] = data[len(line[0]):-1]
