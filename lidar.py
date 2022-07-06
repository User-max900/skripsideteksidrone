#!/usr/bin/env python

import roslib
#roslib.load_manifest('learning_tf')
import rospy
import math
import math
import dronekit
from pymavlink import mavutil
import time

print ("import success")
connection_string = 'udp:127.0.0.1:14550'
print ("set connection_string")
vehicle = dronekit.connect(connection_string, wait_ready=True, timeout=150)
print ("connection_string success")

while True:
    print("Altitude: {0:.2f}m".format(vehicle.rangefinder.distance))


