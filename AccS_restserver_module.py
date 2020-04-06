#!/usr/bin/env python

'''
Justin
'''

import time
import json
import socket
from threading import Thread

from flask import Flask
from flask_table import Table, Col
from werkzeug.serving import make_server
from subprocess import check_output
from AccS_module import AccS_module

class restserver_module(AccS_module) :
    def __init__(self,accS):
        super(restserver_module, self).__init__(accS, "restserver")

    def onStart (self) :
        self.restserver = RestServer(self.accS)
        self.restserver.set_ip_port("0.0.0.0",5000)
        self.restserver.start()
        
    def onStop (self) :
        self.restserver.stop()
        
class ItemTable (Table) :
    name = Col('Name')
    val = Col('Value')
    stat = Col('Status')
    
class ItemEntry(object):
    def __init__(self, name, val, stat) :
        self.name = name
        self.val = val
        self.stat = stat
        
class RestServer():
    '''Rest Server'''
    def __init__(self,accS):
        # Set log level and remove flask output
        import logging
        self.log = logging.getLogger('werkzeug')
        self.log.setLevel(logging.ERROR)

        # Server variables
        self.app = None
        self.run_thread = None
        self.address = 'localhost'
        self.port = 5000
        self.accS = accS
        # Save status
        self.status = None
        self.server = None

    def update(self) :
        self.status = self.getData()
        
    def formatOutput(self, itemList) :
        items = []
        for d in itemList :
            items.append(ItemEntry(name=d[0],val=d[1],stat=d[2]))
            
        table = ItemTable(items)
        return (table.__html__())

    def getData(self) :
        return self.accS.dataDic

    def set_ip_port(self, ip, port):
        '''set ip and port'''
        self.address = ip
        self.port = port
        self.stop()
        self.start()

    def start(self):
        '''Stop server'''
        # Set flask
        self.app = Flask('RestServer')
        self.add_endpoint()
        # Create a thread to deal with flask
        self.run_thread = Thread(target=self.run)
        self.run_thread.start()

    def running(self):
        '''If app is valid, thread and server are running'''
        return self.app != None

    def stop(self):
        '''Stop server'''
        self.app = None
        if self.run_thread:
            self.run_thread = None
        if self.server:
            self.server.shutdown()
            self.server = None

    def run(self):
        '''Start app'''
        self.server = make_server(self.address, self.port, self.app, threaded=True)
        self.server.serve_forever()

    def request2(self, arg=None):
        '''Deal with requests'''
        print("dealing with request", arg)
        if not self.status:
            return '{"result": "No message"}'

        try:
            self.update()
            #return self.formatOutput(self.status)  
        except Exception as e:
            print(e)
            return

        # If no key, show all data
        if not arg:
            return self.formatOutput(self.status)
        
        # display as many items as the user asks for
        args = arg.split('/')
        items = []
        for key in args:
            for d in range(len(self.status)) :
                if (key == self.status[d][0]) :
                    items.append(self.status[d])
                    break
                
        return self.formatOutput(items)

    def request(self, arg=None) :
        print("handling request")
        # if no args, send all we have
        response = "<pre>"
        if arg == None :
            response += str(json.dumps(self.accS.dataDic,indent=0))
        else :
            newDict = {}
            args = arg.split('/')
            for key in args :
                #if key in newDict :
                 #   newDict = newDict[key]
                if (key in self.accS.dataDic) :
                    newDict[key] = self.accS.dataDic[key]
                    #response += str(key) + ":" + str(self.accS.dataDic[key]) + '\n'
            # let user know if none of their input matches a key        
        #if len(response) == 0 :
            #response = "no matching keys"
            response += str(json.dumps(newDict,indent=0))
        return response + "</pre>"
    
    def add_endpoint(self):
        '''Set endpoits'''
        self.app.add_url_rule('/rest/<path:arg>', 'rest', self.request)
        self.app.add_url_rule('/rest/', 'rest', self.request)


