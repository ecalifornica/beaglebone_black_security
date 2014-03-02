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
            # Deadbolt locked.
            if locked and self.locked != None:
                #kitchen_video_handler.video_armed = True
                data = {self.location: locked}
                print(data)
                with requests.Session() as session:
                    try:
                        request = session.post(baseurl, data=json.dumps(data), timeout=requests_timeout)
                        #returned_json = request.json()
                        #print(returned_json['timestamp']
                        #kitchen_video_handler.timestamp = returned_json['timestamp']
                    except:
                        log.debug('REQUEST FAILED')
            # Deadbolt unlocked.
            if not locked and self.locked != None:
                #kitchen_video_handler.video_armed = True
                data = {self.location: locked}
                with requests.Session() as session:
                    try:
                        session.post(baseurl, data=json.dumps(data))
                    except:
                        log.debug('REQUEST FAILED')

            self.locked = locked
