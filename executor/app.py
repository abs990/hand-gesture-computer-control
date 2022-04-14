"""
Executor API for hand-gesture computer control
"""
import json
import os
import sys
import logging
import socket

from flask import Blueprint, Flask, jsonify, request

from db_handler import DB_Handler
from mouse_handler import *
from special_handler import *

db_name = "executor.db"
db_handle = DB_Handler(db_name)

unity_socket = None

#The application
app = Flask(__name__)

#blueprint
bp = Blueprint('app', __name__)

PREFIX_OPEN_COMMAND = "open "
PREFIX_CLOSE_COMMAND = "pkill -x "

UNITY_HOST = '127.0.0.1'
UNITY_PORT = 25002

"""
Endpoint to get app info based on gesture id
"""
@bp.route('/gesture/<gesture_id>/app-info', methods=['GET'])
def get_app_info(gesture_id):
    response = {}
    resp_code = 200
    app_id, app_name = db_handle.get_app_details(int(gesture_id))
    if app_id == "":
        resp_code = 404
    response['app_id'] = app_id
    response['app_name'] = app_name    
    return jsonify(response), resp_code

"""
Endpoint to open app using app id
"""
@bp.route('/app/<app_id>/open', methods=['POST'])
def open_app(app_id):
    response = {}
    app_name = db_handle.get_app_path(int(app_id))
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
    app_name = db_handle.get_canonical_app_name(int(app_id))
    if app_name == None:
        response['message'] = ""
        resp_code = 404
    else:    
        command = PREFIX_CLOSE_COMMAND+app_name
        os.system(command)
        response['message'] = 'Closed'
        resp_code = 200
    return jsonify(response), resp_code

"""
Endpoint to get list of all registered apps
"""
@bp.route('/app/list', methods=['GET'])
def get_all_apps():
    return jsonify(db_handle.get_app_list()), 200

"""
Endpoint to move mouse
"""
@bp.route('/mouse/move', methods=['POST'])
def move_mouse():
    response = {}
    resp_code = 200
    pos_x = request.json.get('pos_x',None)
    pos_y = request.json.get('pos_y',None)
    mouse_move(pos_x,pos_y)
    response['message'] = 'Moved'
    return jsonify(response), resp_code

"""
Endpoint to left click mouse
"""
@bp.route('/mouse/left-click', methods=['POST'])
def left_click_mouse():
    response = {}
    resp_code = 200
    pos_x = request.json.get('pos_x',None)
    pos_y = request.json.get('pos_y',None)
    left_mouse_click(pos_x, pos_y)
    response['message'] = 'Clicked'
    return jsonify(response), resp_code

"""
Endpoint to right click mouse
"""
@bp.route('/mouse/right-click', methods=['POST'])
def right_click_mouse():
    response = {}
    resp_code = 200
    pos_x = request.json.get('pos_x',None)
    pos_y = request.json.get('pos_y',None)
    right_mouse_click(pos_x, pos_y)
    response['message'] = 'Clicked'
    return jsonify(response), resp_code

"""
Endpoint to execute special gesture
"""
@bp.route('/app/<app_id>/special-gesture/<gesture_id>', methods=['POST'])
def trigger_special_gesture(app_id, gesture_id):
    response = {}
    resp_code = 200
    gesture_details = db_handle.get_special_gesture_details(app_id, gesture_id)

    if gesture_details == "":
        return jsonify("Gesture not found"), 404

    if gesture_details['system_hook'] == 'Keyboard':
        key_list = gesture_details['hook_value']
        key_list = key_list.split(',')
        for key in key_list:
            trigger_keyboard_key(key)

    if gesture_details['system_hook'] == 'Shell':
        trigger_shell_command(gesture_details['command'])

    if gesture_details['system_hook'] == 'Unity':
        global unity_socket
        if unity_socket == None:
            try:
                unity_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                unity_socket.connect((UNITY_HOST, UNITY_PORT))
            except Exception as e:
                print("Something's wrong with %s:%d. Exception is %s" % (UNITY_HOST, UNITY_PORT, e))
        try:
            trigger_unity_action(unity_socket, gesture_details['hook_value'])
            response['message'] = 'Triggered'
        except Exception as e:
            print("Something's wrong with %s:%d. Exception is %s" % (UNITY_HOST, UNITY_PORT, e))
            response['message'] = 'Problematic connection to Unity'
            resp_code = 503
            unity_socket.close()
            unity_socket = None

    return jsonify(response), resp_code

"""
Management APIs for gestures
"""
@bp.route('/gesture/register', methods=['POST'])
def register_gesture():
    db_handle.add_gesture(request.json)
    return "Done", 200

@bp.route('/gesture/<gesture_id>', methods=['DELETE'])
def delete_gesture(gesture_id):
    gesture_details = db_handle.get_gesture_details(int(gesture_id))
    if gesture_details == "":
        return jsonify("Gesture not found"), 404
    db_handle.delete_gesture(int(gesture_id))
    return "Done", 200

@bp.route('/gesture/<gesture_id>', methods=['GET'])
def get_gesture_details(gesture_id):
    gesture_details = db_handle.get_gesture_details(int(gesture_id))
    if gesture_details == "":
        return jsonify("Gesture not found"), 404
    return jsonify(gesture_details), 200

"""
Management APIs for special gestures
"""
@bp.route('/app/special-gesture', methods=['POST'])
def add_special_gesture():
    db_handle.add_special_gesture_details(request.json)
    return "Done", 200

@bp.route('/app/special-gesture/<app_id>/<gesture_id>', methods=['GET'])
def get_special_gesture_details(app_id, gesture_id):
    special_gesture_details = db_handle.get_special_gesture_details(int(app_id), int(gesture_id))
    if special_gesture_details == "":
        return jsonify("Special gesture not found"), 404
    return jsonify(special_gesture_details), 200

@bp.route('/app/special-gesture/<app_id>/<gesture_id>', methods=['DELETE'])
def delete_special_gesture(app_id, gesture_id):
    special_gesture_details = db_handle.get_special_gesture_details(int(app_id), int(gesture_id))
    if special_gesture_details == "":
        return jsonify("Special gesture not found"), 404
    db_handle.delete_special_gesture_details(int(app_id), int(gesture_id))
    return "Done", 200

#Register blueprint
app.register_blueprint(bp, url_prefix='/api/v1/executor/')

if __name__ == '__main__':
    if len(sys.argv) < 2:
        logging.error("Usage: app.py <service-port>")
        sys.exit(-1)
    p = int(sys.argv[1])
    # Do not set debug=True---that will disable the Prometheus metrics
    app.run(host='0.0.0.0', port=p, threaded=True, debug=True)            