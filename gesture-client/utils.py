import socket
import logging

server_ok_response = "OK"

def convertDictToMessage(source):
    message = "KP|"
    for key in source.keys():
        value = source[key]
        if value != None:
            message += str(key)
            message += ','
            message += str(value[0])
            message += ','
            message += str(value[1])  
            message += '|'
    message = message[:-1]
    message = message.encode("UTF-8")
    return message    

class ServerChannel:
    def __init__(self, host='127.0.0.1', port=25000, autoconnect = False):
        self.server_host = host
        self.server_port = port
        self.connected = False
        if autoconnect:
            self.connectToAgent()   

    def connectToAgent(self):
        if not self.connected:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                self.sock.connect((self.server_host, self.server_port))
                self.connected = True
            except socket.error as ex:
                self.connected = False
                print(ex)  

    def closeAgent(self):
        if self.connected:
            self.sock.close()
            self.connected = False

    def killAgent(self):
        if self.connected:
            self.sock.shutdown()
            self.connected = False        

    def sendLandmarks(self, landmarks):
        if self.connected:
            self.sock.sendall(convertDictToMessage(landmarks))
            response = self.sock.recv(1024)
            response = response.decode("UTF-8")
            if response != server_ok_response:
                print(response)
