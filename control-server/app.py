"""
Control server module for hand gesture control
"""
import os
from dotenv import load_dotenv
import socket
from gesture_handler import GestureHandler

def server_process(host: str, port: int, rcv_buffer_size: int, sensitivity: int, exec_endpoint: str):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host,port))
    print("Wiaiting for client to connect")
    sock.listen()
    conn, addr = sock.accept()
    with conn:
        print("Client connected")
        handler = GestureHandler(sensitivity=sensitivity, exec_endpoint=exec_endpoint)
        print("Sensitivity =",handler.sensitivity)
        while True:
            msg = conn.recv(rcv_buffer_size)
            msg = msg.decode("UTF-8")
            reply = handler.updateLandmarks(msg)
            conn.sendall(reply.encode("UTF-8"))

if __name__ == '__main__':
    load_dotenv()
    server_process(host=os.getenv('CONTROL_SERVER_HOST'), \
                   port=int(os.getenv('CONTROL_SERVER_PORT')), \
                   rcv_buffer_size=int(os.getenv('CONTROL_SERVER_BUFFER_SIZE')), \
                   sensitivity=int(os.getenv('HANDLER_SENSITIVITY')), \
                   exec_endpoint=os.getenv('EXECUTOR_BASE_ENDPOINT'))