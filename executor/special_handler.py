import os
import keyboard

def trigger_keyboard_key(key):
    keyboard.press_and_release(key)

def trigger_shell_command(command):
    os.system(command)

def trigger_unity_action(unity_socket, message):
    message = message.encode("UTF-8")
    unity_socket.sendall(message)
    response = unity_socket.recv(1024)
    response = response.decode("UTF-8")
    print(response)