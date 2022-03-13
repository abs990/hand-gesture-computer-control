"""
Control server module for hand gesture control
"""
import os
from dotenv import load_dotenv
import socket

LOG_WAITING_FOR_CONNECTION = ""
LOG_CLIENT_CONNECTED = ""
MSG_KP_OK = ""
PREFIX_OPEN_APP_PROMPT = ""
PREFIX_CLOSE_APP_PROMPT = ""
PREFIX_OPENED_APP_NOTIFICATION = ""
PREFIX_CLOSED_APP_NOTIFICATION = ""
SUFFIX_PROMPT = ""

def server_process(host: str, port: int, rcv_buffer_size: int):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host,port))
    print(LOG_WAITING_FOR_CONNECTION)
    sock.listen()
    conn, addr = sock.accept()
    with conn:
        print(LOG_CLIENT_CONNECTED)
        while True:
            msg = conn.recv(rcv_buffer_size)
            msg = msg.decode("UTF-8")
            conn.sendall(MSG_KP_OK.encode("UTF-8"))
    pass

if __name__ == '__main__':
    load_dotenv()
    LOG_WAITING_FOR_CONNECTION = os.getenv('LOG_WAITING_FOR_CONNECTION')
    LOG_CLIENT_CONNECTED = os.getenv('LOG_CLIENT_CONNECTED')
    MSG_KP_OK = os.getenv('MSG_KP_OK')
    PREFIX_OPEN_APP_PROMPT = os.getenv('PREFIX_OPEN_APP_PROMPT')
    PREFIX_CLOSE_APP_PROMPT = os.getenv('PREFIX_CLOSE_APP_PROMPT')
    PREFIX_OPENED_APP_NOTIFICATION = os.getenv('PREFIX_OPENED_APP_NOTIFICATION')
    PREFIX_CLOSED_APP_NOTIFICATION = os.getenv('PREFIX_CLOSED_APP_NOTIFICATION')
    SUFFIX_PROMPT = os.getenv('SUFFIX_PROMPT')
    server_process(host=os.getenv('CONTROL_SERVER_HOST'), \
                   port=int(os.getenv('CONTROL_SERVER_PORT')), \
                   rcv_buffer_size=int(os.getenv('CONTROL_SERVER_BUFFER_SIZE')))