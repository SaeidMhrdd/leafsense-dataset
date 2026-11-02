import subprocess
import sys
import os
import time
import paho.mqtt.publish as publish

size = ''
host = str(sys.argv[2])
channel_num = str(sys.argv[3])
name = str(sys.argv[4])
mess = name + " (CH-" + channel_num + ") -> PKTS of SIZE: "
while True:
    try:
        time.sleep(3)
        statinfo = os.stat(str(sys.argv[1]))
        if str(statinfo) != size:
            print(" PKTS of SIZE: " + str(statinfo.st_size) + ' ' + 'bytes CAPTURED')
            publish.single("status", mess + str(round(float(statinfo.st_size)/1000000,3)) + ' MB CAPTURED', hostname=host)
            size = str(statinfo)
    except:
        publish.single("/mamila", "Awaiting file creation...")
        time.sleep(1)
        continue
