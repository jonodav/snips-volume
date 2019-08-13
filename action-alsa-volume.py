#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from snipsTools import SnipsConfigParser
from hermes_python.hermes import Hermes
from hermes_python.ontology import *
import io
import socket
import random
from subprocess import call

CONFIG_INI = "config.ini"

# If this skill is supposed to run on the satellite,
# please get this mqtt connection info from <config.ini>
# Hint: MQTT server is always running on the master device
MQTT_IP_ADDR = "localhost"
MQTT_PORT = 1883
MQTT_ADDR = "{}:{}".format(MQTT_IP_ADDR, str(MQTT_PORT))

success_tts = ['Got it', 'Sure', 'Done', 'Ok']
fail_tts = ["Sorry, I can't do that", "Sorry, that doesn't work"]
no_slot_tts = ["What do you mean?", "Don't waste my time", "I can't do anything with that", "Please stop bothering me", "No"]

class ALSAVolume(object):
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
    def setVolumeCallback(self, hermes, intent_message):
        # terminate the session first if not continue
        #hermes.publish_end_session(intent_message.session_id, "")

        # action code goes here...
        print '[Received] intent: {}'.format(intent_message.intent.intent_name)
        volumeSet = False

        for (slot_value, slot) in intent_message.slots.items():
            if slot_value == "Volume":
                self.Volume = slot.first().value.encode("utf8")
                volumeSet = True

        if volumeSet:
            print("volumeSet is true")
            try:
                volume = int(self.Volume)
                deviceName = self.config['secret']['deviceName']
                call(["amixer", "set", deviceName, str(volume)+"%"])
            except ValueError:
                pass
            tts = random.choice(success_tts)
        else:
            if(self.config['secret']['snarkyResponses']) == "y":
                tts = random.choice(no_slot_tts)
            else:
                tts = random.choice(fail_tts)
        
        hermes.publish_end_session(intent_message.session_id, tts)

    # --> Master callback function, triggered everytime an intent is recognized
    def master_intent_callback(self,hermes, intent_message):
        coming_intent = intent_message.intent.intent_name
        if coming_intent == 'thejonnyd:SetVolume':
            self.setVolumeCallback(hermes, intent_message)

        # more callback and if condition goes here...

    # --> Register callback function and start MQTT
    def start_blocking(self):
        with Hermes(MQTT_ADDR) as h:
            h.subscribe_intents(self.master_intent_callback).start()
 
if __name__ == "__main__":
    ALSAVolume()
