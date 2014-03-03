import logging
import requests
import time

requests_timeout = 10

class DeadboltHandler(object):
    '''Deadbolt sensor switch.'''
    def __init__(self, location):
        self.location = location
        self.locked = None

    def record(self, locked, log):
        # If lock sensor state has changed.
        if self.locked != locked:
            # Log event.
            now = time.localtime()
            event_data = '%s, %s, %s' % (time.strftime('%Y-%m-%d, %H:%M:%S', now), self.location, 'LOCKED' if locked else 'UNLOCKED')
            log.debug(event_data)
            data = {self.location: 'LOCKED' if locked else 'UNLOCKED'}
            # Deadbolt locked.
            if locked and self.locked != None:
                #kitchen_video_handler.video_armed = True
                with requests.Session() as session:
                    try:
                        request = session.post(baseurl, data=json.dumps(data), timeout=requests_timeout)
                        returned_json = request.json()
                        print(returned_json['timestamp'])
                        #kitchen_video_handler.timestamp = returned_json['timestamp']
                    except:
                        log.debug('REQUEST FAILED')
            # Deadbolt unlocked.
            if not locked and self.locked != None:
                #data = {self.location: locked}
                with requests.Session() as session:
                    try:
                        request = session.post(baseurl, data=json.dumps(data))
                    except:
                        log.debug('REQUEST FAILED')
            self.locked = locked


def post_to_api(log):
    with requests.Session() as session:
        try:
            request = session.post(baseurl, data=json.dumps(data), timeout=requests_timeout)
            returned_json = request.json['timestamp']
            return returned_json
        except:
            log.debug('REQUEST FAILED')


def log_sensor_event(log):
    now = time.localtime()
    event_data = '%s, %s, %s' % (time.strftime('%Y-%m-%d, %H:%M:%S', now), self.location, 'CLOSED' if closed else 'OPEN')
    log.debug(event_data)


class DoorHandler(object):
    '''Door sensor reed switch.'''
    def __init__(self, location):
        self.location = location
        self.closed = None

    def record(self, closed, log):
        if self.closed != closed:
            log_sensor_event(log)
            data = {self.location: 'CLOSED' if closed else 'OPEN'}
            if self.closed != None:
                post_to_api(log)
            self.closed = closed
