#!/usr/bin/env python

import roslib
#roslib.load_manifest('learning_tf')
import rospy
import math
import tf
import rospy
import math
import dronekit
import dronekit_sitl
from pymavlink import mavutil
import time
out=1500
out2=1500
tVTOL1_now = 0
use_px = 1
dropingcount = 0
if use_px == 1:
    def move(a,b,c,d,e,f):
        i=0
        while i<e:
            vehicle.channels.overrides[1] = int(a)
            vehicle.channels.overrides[2] = int(b)
            vehicle.channels.overrides[3] = int(c)
            print (i)
            print (f)
            i=i+1
            time.sleep(0.1)

if use_px==1:
    print ("import success")
    connection_string = 'udp:127.0.0.1:14550'
    print ("set connection_string")
    vehicle = dronekit.connect(connection_string, wait_ready=True, timeout=150)
    print ("connection_string success")

    vehicle.mode = dronekit.VehicleMode('LOITER')
    print("sudah loiter yas")
    print("Waitting the drone is armed")
    while not vehicle.armed:
        time.sleep(0.5)

    print("Drone is ARMED")
    time.sleep(1)

    print("Taking off")
    while True:
#        move(1500,1500,1620,1500)
        vehicle.channels.overrides[3] = 1630
        vehicle.channels.overrides[1] = 1500
        vehicle.channels.overrides[2] = 1500
        if vehicle.rangefinder.distance >= 1.0:
            print('Reached target altitude: {0:.2f}m'.format(vehicle.rangefinder.distance))
            move(1500,1500,1500,1500,10,"Hover")
            break
        else:
            print("Altitude: {0:.2f}m".format(vehicle.rangefinder.distance))
        time.sleep(0.25)


rospy.init_node('drone_tf_listener')
# move(1500,1500,1500,1500,1,"Hover")

listener = tf.TransformListener()
# move(1500,1500,1500,1500,1,"Hover")

rate = rospy.Rate(10.0)
while not rospy.is_shutdown():
    
    if use_px == 1:
        if tVTOL1_now==0:
            vehicle.channels.overrides[3] = 1500
            vehicle.channels.overrides[1] = 1500
            vehicle.channels.overrides[2] = 1500
            time.sleep(0.25)

    try:
        (trans,rot) = listener.lookupTransform('/drone', '/ilyastf', rospy.Time(0))
        tVTOL1_now = trans[0]
        x_axis = trans[0]
        y_axis = trans[1]
        if(x_axis>70):
            out=1450
        if(x_axis<-70):
            out=1550
        if(y_axis>50):
            out2=1450
        if(y_axis<-50):
            out2=1550
        if(x_axis>-70 and x_axis<70):
            out=1500
        if(y_axis>-50 and y_axis<50):
            out2=1500
        print (str(out)+"    "+str(out2))



    # time.sleep(1)
        print("y : "+str(y_axis)+str("   x : ")+str(x_axis))
    
    except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
        continue
    if tVTOL1_now != 0:
        if x_axis > -70 and x_axis <70 and y_axis > -50 and y_axis < 50 :
        	#-70>x>70
            print ("sudah di tengah")
            dropingcount = dropingcount+1
            print (dropingcount)
    # out, out2 = getFuzzy(x_axis,y_axis)

    print ("out "+str(out))
    print ("out2 "+str(out2))

    if use_px == 1:
        vehicle.channels.overrides[3] = 1500
        vehicle.channels.overrides[1] = int(out)
        vehicle.channels.overrides[2] = int(out2)
    if dropingcount > 2:
        break


if use_px==1:
    print("Hover")
    move(1500,1500,1500,1500,10,"Hover")
    print("Setting LAND mode...")
    vehicle.mode = dronekit.VehicleMode('LAND')
    time.sleep(2)

    # Close vehicle object before exiting script
    print("Close vehicle object")
    vehicle.close()
# break        
print("masuk rosshutdown")
