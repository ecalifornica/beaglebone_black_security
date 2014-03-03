import logging
import requests
import time

requests_timeout = 10


def post_to_api(log):
    with requests.Session() as session:
        try:
            request = session.post(baseurl, data=json.dumps(data), timeout=requests_timeout)
            returned_json = request.json['timestamp']
            return returned_json
        except:
            log.debug('REQUEST FAILED')


def log_sensor_event(self, log, sensor_state):
    now = time.localtime()
    event_data = '%s, %s, %s' % (time.strftime('%Y-%m-%d, %H:%M:%S', now), self.location, sensor_state)
    log.debug(event_data)


class DoorHandler(object):
    '''Door sensor reed switch.'''
    def __init__(self, location):
        self.location = location
        self.closed = None

    def record(self, closed, log):
        if self.closed != closed:
            sensor_state = 'CLOSED' if closed else 'OPEN'
            log_sensor_event(self, log, sensor_state)
            data = {self.location: sensor_state}
            if self.closed != None:
                post_to_api(log)
            self.closed = closed


class DeadboltHandler(object):
    '''Deadbolt sensor switch.'''
    def __init__(self, location):
        self.location = location
        self.locked = None

    def record(self, locked, log):
        # If lock sensor state has changed.
        if self.locked != locked:
            sensor_state = 'LOCKED' if locked else 'UNLOCKED'
            log_sensor_event(self, log, sensor_state)
            data = {self.location: sensor_state}
            if self.locked != None:
                #kitchen_video_handler.video_armed = True
                post_to_api(log)
            self.locked = locked


