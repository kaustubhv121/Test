#!/usr/bin/env python

import obd_io
import serial
import platform
import obd_sensors
from datetime import datetime
import time
import getpass


from obd_utils import scanSerial

class OBD_Recorder():
    def __init__(self, path, log_items):
        self.port = None
        self.sensorlist = []
        localtime = time.localtime(time.time())
        filename = path+"car-"+str(localtime[0])+"-"+str(localtime[1])+"-"+str(localtime[2])+"-"+str(localtime[3])+"-"+str(localtime[4])+"-"+str(localtime[5])+".log"
        self.log_file = open(filename, "w", 128)
        self.log_file.write("ERROR CODES\n");

        for item in log_items:
            self.add_log_item(item)

    def connect(self):
        portnames = scanSerial()

        for port in portnames:
            self.port = obd_io.OBDPort(port, None, 2, 2)
            if(self.port.State == 0):
                self.port.close()
                self.port = None
            else:
                break
            
    def is_connected(self):
        return self.port
        
    def add_log_item(self, item):
        for index, e in enumerate(obd_sensors.SENSORS):
            if(item == e.shortname):
                self.sensorlist.append(index)
                break
            
            
    def record_data(self):
        if(self.port is None):
            return None
       
        while 1:
            for index in self.sensorlist:
                (name, value, unit) = self.port.sensor(index)
            self.log_file.write(str(value)+"\n")
            print str(value)+"\n"
            
username = getpass.getuser()  
logitems = ["dtc_status"]
o = OBD_Recorder('/home/'+username+'/Test/log/', logitems)
o.connect()

if not o.is_connected():
    print "Not connected"
o.record_data()
