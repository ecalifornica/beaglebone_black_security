from flask import Flask, jsonify, render_template, request
import json
import os
import time
import logging

app = Flask(__name__)
app.config['DEBUG'] = True
host = os.environ['FLASK_HOST']
port = int(os.environ['FLASK_PORT'])


@app.route('/security/', methods=['POST'])
def sensor_input():
    if request.method == 'POST':
        #posted_data = json.loads(request.data)
        now = time.localtime()
        timestamp = time.strftime('%Y-%m-%d, %H:%M:%S', now)
        posted_data = request.get_json(force=True)
        posted_data_key = posted_data.keys()[0]
        posted_data_value = posted_data.values()[0]
        log.debug('%s, %s, %s' % (timestamp, posted_data_key, posted_data_value))

        try:
            with open('sensors.json', 'r') as json_file:
                json_data = json.load(json_file)
        except:
            json_data = {}
        
        json_data[posted_data_key] = posted_data_value
        json_data['timestamp'] = timestamp

        with open('sensors.json', 'w') as json_file:
            json.dump(json_data, json_file)
        return jsonify(json_data)

@app.route('/ajax/')
def ajax():
    try:
        with open('sensors.json', 'r') as json_file:
            json_data = json.load(json_file)
    except:
        json_data = {'no data': 'lol'}
    return jsonify(json_data)

@app.route('/', methods=['GET'])
def user_interface():
    return render_template('index.html')


def main():
    app.run(host, port, threaded=True)


if __name__ == '__main__':
    # Logging setup.
    now = time.strftime('%Y-%m-%d, %H:%M:%S', time.localtime())
    log = logging.getLogger(__name__)
    logging.basicConfig(level=logging.DEBUG)
    log.setLevel(logging.DEBUG)
    logfile = logging.FileHandler('server.log')
    logfile.setLevel(logging.DEBUG)
    log.addHandler(logfile)
    log.debug('%s, SYSTEM, API START' % now)
    main()
