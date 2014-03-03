'''
Refactored BBB node.
'''

import os
import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.PWM as PWM
import time
import logging
#import requests
from subprocess import call
import json
from lib import DeadboltHandler, DoorHandler

baseurl = os.environ['BASEURL']
requests_timeout = 10
kitchen_PIR_gpio_pin = 'P8_7'
deadbolt_gpio_pin = 'P8_9'
back_door_gpio_pin = 'P8_11'


if __name__ == '__main__':
    now = time.strftime('%Y-%m-%d, %H:%M:%S', time.localtime())
    # Logging setup.
    log = logging.getLogger(__name__)
    logging.basicConfig(level=logging.DEBUG)
    log.setLevel(logging.DEBUG)
    logfile = logging.FileHandler('refactor.log')
    logfile.setLevel(logging.DEBUG)
    log.addHandler(logfile)
    log.debug('%s, PROGRAM START' % now)
    # GPIO setup.
    GPIO.setup(deadbolt_gpio_pin, GPIO.IN)
    GPIO.setup(back_door_gpio_pin, GPIO.IN)
    GPIO.setup(kitchen_PIR_gpio_pin, GPIO.IN)

    deadbolt_handler = DeadboltHandler('BACK DOOR')
    back_door_handler = DoorHandler('BACK DOOR')

    while True:
        '''
        with open('node_config.json', 'r') as node_config_file:
            node_config = json.load(node_config_file)
        '''
        deadbolt_handler.record(GPIO.input(deadbolt_gpio_pin), log)
        back_door_handler.record(GPIO.input(back_door_gpio_pin), log)
        # Threaded video capture

        time.sleep(.1)
        
