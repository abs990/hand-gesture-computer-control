"""
Executor API for hand-gesture computer control
"""
import os
import sys
import logging

from flask import Blueprint, Flask, jsonify, request

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

"""
Endpoint to move mouse
"""
@bp.route('/mouse/move', methods=['POST'])
def move_mouse():
    response = {}
    resp_code = 200
    pos_x = request.json.get('pos_x',None)
    pos_y = request.json.get('pos_y',None)
    handle.mouse_move(pos_x,pos_y)
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
    handle.left_mouse_click(pos_x, pos_y)
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
    handle.right_mouse_click(pos_x, pos_y)
    response['message'] = 'Clicked'
    return jsonify(response), resp_code

app.register_blueprint(bp, url_prefix='/api/v1/executor/')

if __name__ == '__main__':
    if len(sys.argv) < 2:
        logging.error("Usage: app.py <service-port>")
        sys.exit(-1)
    p = int(sys.argv[1])
    # Do not set debug=True---that will disable the Prometheus metrics
    app.run(host='0.0.0.0', port=p, threaded=True, debug=True)            