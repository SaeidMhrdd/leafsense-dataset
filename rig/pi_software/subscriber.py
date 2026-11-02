import paho.mqtt.client as mqtt
import os
import sys
import signal
import paho.mqtt.publish as publish

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    
    #print(sys.argv[1])
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("terminate")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    global host
    print(msg.topic+" "+str(msg.payload))
    if 'terminate' in str(msg.payload):
        print("KILLING Tshark!")
        publish.single("status","Terminating Tshark...",hostname=host)
        os.kill(int(sys.argv[1]), signal.SIGTERM)

        delmon1 = subprocess.check_output(['sudo','iw','dev','mon1','del'])
        publisher("status","Preparing to quit " + str(delmon1),host)

        wlanup = subprocess.check_output(['sudo','iw','phy','phy1','interface','add','wlan1','type','managed'])
        publisher("status","Adding back interface wlan1 " + str(pdown),host)
        print("Adding back interface wlan1 " + str(wlanup))
        
    if 'shutdown' in str(msg.payload):
        print("Shutting down...")
        publish.single("status","Shutting down...",hostname="localhost")
        os.kill(int(sys.argv[1]), signal.SIGTERM)

          
        
host = str(sys.argv[2])
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(host, 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
