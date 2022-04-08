import os
import keyboard

def trigger_keyboard_key(key):
    keyboard.press_and_release(key)

def trigger_shell_command(command):
    os.system(command)