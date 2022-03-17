"""
Executor API for hand-gesture computer control
"""
import os
import sys
import logging

from flask import Blueprint, Flask, jsonify

import handler as handle

#The application
app = Flask(__name__)

#blueprint
bp = Blueprint('app', __name__)

PREFIX_OPEN_COMMAND = "open "
PREFIX_CLOSE_COMMAND = "pkill -x "

"""
Endpoint to get app info based on gesture id
"""
@bp.route('/gesture/<gesture_id>/app-info', methods=['GET'])
def get_app_info(gesture_id):
    response = {}
    resp_code = 200
    app_id, app_name = handle.get_app_details(int(gesture_id))
    if app_id == None:
        resp_code = 404
        response['app_id'] = ""
        response['app_name'] = ""
    else:
        response['app_id'] = app_id
        response['app_name'] = app_name    
    return jsonify(response), resp_code

"""
Endpoint to open app using app id
"""
@bp.route('/app/<app_id>/open', methods=['POST'])
def open_app(app_id):
    response = {}
    app_name = handle.get_app_path(int(app_id))
    if app_name == None:
        response['message'] = ""
        resp_code = 404
    else:    
        command = PREFIX_OPEN_COMMAND+app_name
        os.system(command)
        response['message'] = 'Opened'
        resp_code = 200
    return jsonify(response), resp_code
"""
Endpoint to close app using app id
"""
@bp.route('/app/<app_id>/close', methods=['POST'])
def close_app(app_id):
    response = {}
    app_name = handle.get_canonical_app_name(int(app_id))
    if app_name == None:
        response['message'] = ""
        resp_code = 404
    else:    
        command = PREFIX_CLOSE_COMMAND+app_name
        os.system(command)
        response['message'] = 'Closed'
        resp_code = 200
    return jsonify(response), resp_code

app.register_blueprint(bp, url_prefix='/api/v1/executor/')

if __name__ == '__main__':
    if len(sys.argv) < 2:
        logging.error("Usage: app.py <service-port>")
        sys.exit(-1)
    p = int(sys.argv[1])
    # Do not set debug=True---that will disable the Prometheus metrics
    app.run(host='0.0.0.0', port=p, threaded=True, debug=True)            