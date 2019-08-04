#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from snipsTools import SnipsConfigParser
from hermes_python.hermes import Hermes
from hermes_python.ontology import *
import io
import socket
import random

CONFIG_INI = "config.ini"

# If this skill is supposed to run on the satellite,
# please get this mqtt connection info from <config.ini>
# Hint: MQTT server is always running on the master device
MQTT_IP_ADDR = "localhost"
MQTT_PORT = 1883
MQTT_ADDR = "{}:{}".format(MQTT_IP_ADDR, str(MQTT_PORT))

success_tts = ['Got it', 'Sure', 'Done', 'Ok']
fail_tts = ["Sorry, I can't do that", "Sorry, that doesn't work", "No"]

class SmartDevices(object):
    """Class used to wrap action code with mqtt connection
        
        Please change the name refering to your application
    """

    def __init__(self):
        # get the configuration if needed
        try:
            self.config = SnipsConfigParser.read_configuration_file(CONFIG_INI)
        except :
            self.config = None

        # start listening to MQTT
        self.start_blocking()
        
    # --> Sub callback function, one per intent
    def onOffCallback(self, hermes, intent_message):
        # terminate the session first if not continue
        #hermes.publish_end_session(intent_message.session_id, "")
        
        # action code goes here...
        print '[Received] intent: {}'.format(intent_message.intent.intent_name)

        # get the slots from intent
        for (slot_value, slot) in intent_message.slots.items():
            if slot_value == "Device":
                self.Device = slot.first().value.encode("utf8")
            if slot_value == "State":
                self.State = slot.first().value.encode("utf8")

        data = None

        if self.Device == "downlights":
            ip = "192.168.0.160"
            port = 16000
            if self.State == "On":
                data = "1"
            if self.State == "Off":
                data = "0"
        if self.Device == "desk light":
            ip = "192.168.0.181"
            port = 4221
            if self.State == "Off":
                data = "f,0,0,0,0,0"
            if self.State == "On":
                data = "f,0,0,0,0,255"
        if self.Device == "bedside lamp":
            ip = "192.168.0.180"
            port = 4220
            if self.State == "Off":
                data = "f,0"
            if self.State == "On":
                data = "f,255"
        if self.Device == "smart lamp":
            ip = "192.168.0.182"
            port = 4222
            if self.State == "Off":
                data = "f,0,0,0"
            if self.State == "On":
                data = "f,255,255,255"

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
        sock.sendto(data, (ip, port))

        if data is not None:
            tts = random.choice(success_tts)
        else:
            tts = random.choice(fail_tts)
        #tts = "Turned the " + self.Device + " " + self.State

        # if need to speak the execution result by tts
        hermes.publish_end_session(intent_message.session_id, tts)

    def setBrightnessCallback(self, hermes, intent_message):
        # terminate the session first if not continue
        #hermes.publish_end_session(intent_message.session_id, "")

        # action code goes here...
        print '[Received] intent: {}'.format(intent_message.intent.intent_name)

        for (slot_value, slot) in intent_message.slots.items():
            if slot_value == "Device":
                self.Device = slot.first().value.encode("utf8")
            if slot_value == "Brightness":
                self.Brightness = slot.first().value.encode("utf8")

        data = None

        if self.Device == "downlights":
            ip = "192.168.0.160"
            port = 16000
            value = (float(self.Brightness) / 100) * 1023
            data = "l," + str(value)
        
        if self.Device == "bedside lamp":
            ip = "192.168.0.180"
            port = 4220
            value = (float(self.Brightness) / 100) * 255
            data = "f," + str(value)

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
        sock.sendto(data, (ip, port))

        if data is not None:
            tts = random.choice(success_tts)
        else:
            tts = random.choice(fail_tts)
        #tts = self.Device + " set to " + self.Brightness + " percent"

        # if need to speak the execution result by tts
        hermes.publish_end_session(intent_message.session_id, tts)
    
    def setColorCallback(self, hermes, intent_message):
        # terminate the session first if not continue
        #hermes.publish_end_session(intent_message.session_id, "")

        # action code goes here...
        print '[Received] intent: {}'.format(intent_message.intent.intent_name)

        for (slot_value, slot) in intent_message.slots.items():
            if slot_value == "device":
                self.device = slot.first().value.encode("utf8")
            if slot_value == "color":
                self.color = slot.first().value.encode("utf8")

        data = None

        if self.Device == "downlights":
            ip = "192.168.0.160"
            port = 16000
            data = "t," + ctFromColor(self.color)
        
        if self.Device == "desk light":
            ip = "192.168.0.181"
            port = 4221
            data = "f," + rgbctFromColor(self.color)
        
        if self.Device == "smart lamp":
            ip = "192.168.0.182"
            port = 4222
            data = "f," + rgbFromColor(self.color)
            if self.color == "fire":
                data = "b"
            if self.color == "clouds":
                data = "d"
            if self.color == "cycle":
                data = "c"

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
        sock.sendto(data, (ip, port))

        if data is not None:
            tts = random.choice(success_tts)
        else:
            tts = random.choice(fail_tts)
        #tts = self.Device + " set to " + self.Brightness + " percent"

        # if need to speak the execution result by tts
        hermes.publish_end_session(intent_message.session_id, tts)

    def setSceneCallback(self, hermes, intent_message):
        # terminate the session first if not continue
        #hermes.publish_end_session(intent_message.session_id, "")

        # action code goes here...
        print '[Received] intent: {}'.format(intent_message.intent.intent_name)

        for (slot_value, slot) in intent_message.slots.items():
            if slot_value == "Scene":
                self.Scene = slot.first().value.encode("utf8")

        if self.Scene == "day":
            downlightData = "f,1023,1023,1000"
            deskstripData = "f,0,0,0,0,255"
            smartlampData = "g,0,0,100,90,100,0"
            bedlampData = "f,0"
        if self.Scene == "lights out":
            downlightData = "0"
            deskstripData = "f,0,0,0,0,0"
            smartlampData = "f,0,0,0"
            bedlampData = "f,0"
        if self.Scene == "reading":
            downlightData = "0"
            deskstripData = "f,255,0,0,0,0"
            smartlampData = "f,16,0,0"
            bedlampData = "f,5"
        if self.Scene == "blue":
            downlightData = "f,1023,1023,1000"
            deskstripData = "f,0,0,255,0,0"
            smartlampData = "f,0,0,255"
            bedlampData = "f,0"
        if self.Scene == "dim":
            downlightData = "0"
            deskstripData = "f,255,0,0,0,0"
            smartlampData = "f,0,0,0"
            bedlampData = "f,1"
        if self.Scene == "calm":
            downlightData = "f,756,1023,1000"
            deskstripData = "f,0,0,255,0,48"
            smartlampData = "d"
            bedlampData = "f,39"
        if self.Scene == "cozy":
            downlightData = "l,50,0,1000"
            deskstripData = "f,0,0,0,255,0"
            smartlampData = "b"
            bedlampData = "f,128"

        #Set downlights
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
        sock.sendto(downlightData, ("192.168.0.160", 16000))
        #Set desk led strip
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
        sock.sendto(deskstripData, ("192.168.0.181", 4221))
        #Set smart lamp
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
        sock.sendto(smartlampData, ("192.168.0.182", 4222))
        #Set bedside lamp
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
        sock.sendto(bedlampData, ("192.168.0.180", 4220))

        if data is not None:
            tts = random.choice(success_tts)
        else:
            tts = random.choice(fail_tts)
        #tts = self.Device + " set to " + self.Brightness + " percent"

        # if need to speak the execution result by tts
        hermes.publish_end_session(intent_message.session_id, tts)


    # --> Master callback function, triggered everytime an intent is recognized
    def master_intent_callback(self,hermes, intent_message):
        coming_intent = intent_message.intent.intent_name
        if coming_intent == 'thejonnyd:OnOff':
            self.onOffCallback(hermes, intent_message)
        if coming_intent == 'thejonnyd:SetBrightness':
            self.setBrightnessCallback(hermes, intent_message)
        if coming_intent == 'thejonnyd:SetColor':
            self.setColorCallback(hermes, intent_message)
        if coming_intent == 'thejonnyd:SetScene':
            self.setSceneCallback(hermes, intent_message)
        if coming_intent == 'thejonnyd:Leaving':
            self.leavingCallback(hermes, intent_message)

        # more callback and if condition goes here...

    # --> Register callback function and start MQTT
    def start_blocking(self):
        with Hermes(MQTT_ADDR) as h:
            h.subscribe_intents(self.master_intent_callback).start()

    def ctFromColor(color):
        if color == "natural":
            return "512"
        if color == "warm":
            return "0"
        if color == "cool":
            return "1023"
        else:
            return ""
    
    def rgbctFromColor(color):
        if color == "natural":
            return "0,0,0,255,255"
        if color == "warm":
            return "0,0,0,255,0"
        if color == "cool":
            return "0,0,0,0,255"
        if color == "blue":
            return "0,0,255,0,0"
        if color == "green":
            return "0,255,0,0,0"
        if color == "red":
            return "255,0,0,0,0"
        if color == "cyan":
            return "0,255,255,0,0"
        if color == "yellow":
            return "255,255,0,0,0"
        if color == "pink":
            return "255,0,255,0,0"
        else:
            return ""
    
    def rgbFromColor(color):
        if color == "natural":
            return "255,255,255"
        if color == "warm":
            return "255,255,200"
        if color == "cool":
            return "230,230,255"
        if color == "blue":
            return "0,0,255"
        if color == "green":
            return "0,255,0"
        if color == "red":
            return "255,0,0"
        if color == "cyan":
            return "0,255,255"
        if color == "yellow":
            return "255,255,0"
        if color == "pink":
            return "255,0,255"
        else:
             return ""
 
if __name__ == "__main__":
    SmartDevices()
