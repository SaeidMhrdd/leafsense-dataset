import paho.mqtt.client as mqtt
import os
import sys
import signal
import paho.mqtt.publish as publish
import subprocess
import time

global host
global timeUpdates

def conf_extracter():
    global host
    try:
        
        with open('rpi_sense.conf') as f:
    
            for line in f:
                if 'head' in line:
                   host = parser(line)
    except:

        publisher("status","Configuratioin file error",host)
        #shutdown()

def parser(line):
    value = line.split(':')[1].strip()

    return value

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    
    #print(sys.argv[1])
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("time")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    global host
    global timeUpdates
    print(msg.topic+" "+str(msg.payload))
    
    print("Updating time")
    publish.single("status","Time sync...",hostname=host)
   
    updateT = subprocess.check_output(['sudo','date','--set',msg.payload])
    timeUpdates = timeUpdates + 1
    print(updateT)
    if timeUpdates > 5:
       quit()

time.sleep(20)
conf_extracter()
timeUpdates = 0
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(host, 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
