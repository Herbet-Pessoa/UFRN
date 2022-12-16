#!/usr/bin/env python
# File: trabalho.py

import socket
import time
import paho.mqtt.client as mqtt

THE_BROKER = "broker.hivemq.com"
THE_TOPIC = "ufrn/test/trab_IoT"
CLIENT_ID = ""



def levelOfBattery(nSensor, host, port):
    s = socket.socket()
    s.connect((host, port))
    
    if (nSensor == 0):
        s.send('get.sensor1.wintfs[0].consumption'.encode('utf-8'))
    if (nSensor == 1):
        s.send('get.sensor2.wintfs[0].consumption'.encode('utf-8'))
    if (nSensor == 2):
        s.send('get.sensor3.wintfs[0].consumption'.encode('utf-8'))
    
    battery = int(float(s.recv(1024).decode('utf-8'))//1)

    if (battery >= 100):
        battery = 100

    return battery


def infoLevelOfBattery(battery, nSensor):
    if (battery[nSensor] >= 80 and battery[nSensor] <= 83):
        message = ("Sensor" + str(nSensor+1) + " atingiu nível crítico de bateria.")
        return message
    elif (battery[nSensor] >= 100):
        message = ("Sensor" + str(nSensor+1) + " está sem bateria.")
        return message
    else: 
        return ""



def finalMessageBattery(battery, nSensor):
    message = infoLevelOfBattery(battery, nSensor)
    return message


def verifyIfFinished(battery, port):
    if(battery[0] == 100 and battery[1] == 100 and battery[2] == 100):
        return False
    return True


client = mqtt.Client(client_id=CLIENT_ID, 
                     clean_session=True, 
                     userdata=None, 
                     protocol=mqtt.MQTTv311, 
                     transport="tcp")


client.username_pw_set(None, password=None)
client.connect("broker.hivemq.com", port=1883, keepalive=60)

client.loop_start()

battery = [0,0,0]
sensor = 0
continueLoop = True
while continueLoop:

    host = '127.0.0.1'
    nSensor = sensor%3
    battery[nSensor] = levelOfBattery(nSensor, host, port=12345)
    
    msg_to_be_sent = finalMessageBattery(battery, nSensor)
    
    if (nSensor == 0):
        client.publish(THE_TOPIC+"/sensor1", 
                    payload=battery[nSensor], 
                    qos=0, 
                    retain=True)
    elif (nSensor == 1):
        client.publish(THE_TOPIC+"/sensor2", 
                    payload=battery[nSensor], 
                    qos=0, 
                    retain=True)
    elif (nSensor == 2):
        client.publish(THE_TOPIC+"/sensor3", 
                    payload=battery[nSensor], 
                    qos=0, 
                    retain=True)
    
    
    print(str(nSensor), str(battery[nSensor]) + msg_to_be_sent)
    continueLoop = verifyIfFinished(battery, port=12345)
    sensor+=1
    time.sleep(1)



client.loop_stop()
