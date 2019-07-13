#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from snipsTools import SnipsConfigParser
from hermes_python.hermes import Hermes
from hermes_python.ontology import *
import io
import socket

CONFIG_INI = "config.ini"

# If this skill is supposed to run on the satellite,
# please get this mqtt connection info from <config.ini>
# Hint: MQTT server is always running on the master device
MQTT_IP_ADDR = "localhost"
MQTT_PORT = 1883
MQTT_ADDR = "{}:{}".format(MQTT_IP_ADDR, str(MQTT_PORT))

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

        ip = "192.168.0.160"
        port = 16000
        data = "2"
        
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
            ip = "192.168.0.181"
            port = 4221
            if self.State == "Off":
                data = "f,0,0,0,0,0"
            if self.State == "On":
                data = "f,0,0,0,0,255"
        if self.Device == "smart lamp":
            ip = "192.168.0.181"
            port = 4221
            if self.State == "Off":
                data = "f,0,0,0"
            if self.State == "On":
                data = "f,255,255,255"

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
        sock.sendto(data, (ip, port))

        tts = "Turned the " + self.Device + " " + self.State

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

        if self.Device == "downlights":
            ip = "192.168.0.160"
            port = 16000
            value = (float(self.Brightness) / 100) * 1023
            data = "l," + str(value)

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
        sock.sendto(data, (ip, port))

        tts = self.Device + " set to " + self.Brightness + " percent"

        # if need to speak the execution result by tts
        hermes.publish_end_session(intent_message.session_id, tts)

    # More callback function goes here...

    # --> Master callback function, triggered everytime an intent is recognized
    def master_intent_callback(self,hermes, intent_message):
        coming_intent = intent_message.intent.intent_name
        if coming_intent == 'thejonnyd:OnOff':
            self.onOffCallback(hermes, intent_message)
        if coming_intent == 'thejonnyd:SetBrightness':
            self.setBrightnessCallback(hermes, intent_message)

        # more callback and if condition goes here...

    # --> Register callback function and start MQTT
    def start_blocking(self):
        with Hermes(MQTT_ADDR) as h:
            h.subscribe_intents(self.master_intent_callback).start()

if __name__ == "__main__":
    SmartDevices()
