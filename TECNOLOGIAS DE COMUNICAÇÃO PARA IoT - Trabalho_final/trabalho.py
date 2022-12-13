#!/usr/bin/env python
# File: trabalho.py

import socket

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
    
    battery = float(s.recv(1024).decode('utf-8'))

    if (battery >= 100):
        battery = 100

    return battery


def infoLevelOfBattery(level, nSensor):
    if (level > 79.9 and level <= 80.3):
        message = ("Sensor" + str(nSensor) + " atingiu nível crítico de bateria.")
        return message
    elif (level >= 100):
        message = ("Sensor" + str(nSensor) + " está sem bateria.")
        return message
    else: 
        return ""



def finalMessageBattery(battery, nSensor):
    message = str(battery) + infoLevelOfBattery(battery, nSensor)
    return message


def verifyIfFinished(host, port):
    battery = []
    for i in range(0,3):
        battery.append(levelOfBattery(i, host, port))
    
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


sensor = 0
continueLoop = True
while continueLoop:

    host = '127.0.0.1'
    nSensor = sensor%3
    battery = levelOfBattery(nSensor, host, port=12345)

    continueLoop = verifyIfFinished(host, port=12345)
    msg_to_be_sent = finalMessageBattery(battery, nSensor)
    
    if (nSensor == 0):
        client.publish(THE_TOPIC+"/sensor1", 
                    payload=msg_to_be_sent, 
                    qos=0, 
                    retain=True)
    elif (nSensor == 1):
        client.publish(THE_TOPIC+"/sensor2", 
                    payload=msg_to_be_sent, 
                    qos=0, 
                    retain=True)
    elif (nSensor == 2):
        client.publish(THE_TOPIC+"/sensor3", 
                    payload=msg_to_be_sent, 
                    qos=0, 
                    retain=True)
    
    
    print(msg_to_be_sent)
    sensor+=1



client.loop_stop()
