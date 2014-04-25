# Refactored BBB node.

import os
import Adafruit_BBIO.GPIO as GPIO
import time
import logging
from bbb_node_lib import (DeadboltHandler, DoorHandler, MotionHandler,
                          post_to_api)

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
    log.debug('%s, SYSTEM, NODE A START' % now)
    data = {'SYSTEM': 'NODE A START'}
    post_to_api(log, data)
    # GPIO setup.
    GPIO.setup(deadbolt_gpio_pin, GPIO.IN)
    GPIO.setup(back_door_gpio_pin, GPIO.IN)
    GPIO.setup(kitchen_PIR_gpio_pin, GPIO.IN)
    deadbolt_handler = DeadboltHandler('BACKDOORDEADBOLT')
    back_door_handler = DoorHandler('BACKDOOR')
    kitchen_motion_handler = MotionHandler('KITCHENMOTION')
    while True:
        deadbolt_handler.record(GPIO.input(deadbolt_gpio_pin), log)
        back_door_handler.record(GPIO.input(back_door_gpio_pin), log)
        kitchen_motion_handler.record(GPIO.input(kitchen_PIR_gpio_pin), log)
        # Threaded video capture
        time.sleep(.1)
