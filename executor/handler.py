from Quartz.CoreGraphics import CGEventCreateMouseEvent
from Quartz.CoreGraphics import CGEventPost
from Quartz.CoreGraphics import kCGEventMouseMoved
from Quartz.CoreGraphics import kCGEventLeftMouseDown
from Quartz.CoreGraphics import kCGEventLeftMouseUp
from Quartz.CoreGraphics import kCGMouseButtonLeft
from Quartz.CoreGraphics import kCGHIDEventTap
from Quartz.CoreGraphics import kCGMouseButtonRight
from Quartz.CoreGraphics import kCGEventRightMouseDown
from Quartz.CoreGraphics import kCGEventRightMouseUp
from Quartz.CoreGraphics import CGEventSetIntegerValueField
from Quartz.CoreGraphics import kCGMouseEventClickState
from Quartz.CoreGraphics import CGEventSetType
import time

gesture_app_mapper = {
    1: 1,
    2: 2,
    3: 3,
    4: 4
}

app_info = {
    1: "/Applications/Microsoft\ Outlook.app",
    2: "/Applications/Safari.app",
    3: "/Applications/GarageBand.app",
    4: "/Applications/Trello.app"
}

canonical_app_name = {
    1: "Microsoft\ Outlook",
    2: "Safari",
    3: "GarageBand",
    4: "Trello"
}

def get_app_details(gesture_id):
    if gesture_id in gesture_app_mapper:
        app_id = gesture_app_mapper[gesture_id]
        app_name = canonical_app_name[app_id]
        return app_id, app_name
    else:
        return None, None

def get_app_path(app_id):
    if app_id in app_info:
        return app_info[app_id]
    else:
        return None

def get_canonical_app_name(app_id):
    if app_id in canonical_app_name:
        return canonical_app_name[app_id]
    else:
        return None

def mouseEvent(type, posx, posy, button_type):
    theEvent = CGEventCreateMouseEvent(None, type, (posx,posy), button_type)
    CGEventPost(kCGHIDEventTap, theEvent)

def mouse_move(posx,posy):
    mouseEvent(kCGEventMouseMoved, posx, posy, kCGMouseButtonLeft)

def left_mouse_click(posx,posy):
    event = CGEventCreateMouseEvent(
                        None,
                        kCGEventLeftMouseDown,
                        (posx, posy),
                        kCGMouseButtonLeft)

    CGEventSetIntegerValueField(event, kCGMouseEventClickState, 2)
    CGEventPost(kCGHIDEventTap, event)

    CGEventSetType(event, kCGEventLeftMouseUp)
    CGEventPost(kCGHIDEventTap, event)
    CGEventSetType(event, kCGEventLeftMouseDown)
    CGEventPost(kCGHIDEventTap, event)
    CGEventSetType(event, kCGEventLeftMouseUp)
    CGEventPost(kCGHIDEventTap, event)

def right_mouse_click(posx,posy):
    mouseEvent(kCGEventRightMouseDown, posx, posy, kCGMouseButtonRight)
    mouseEvent(kCGEventRightMouseUp, posx, posy, kCGMouseButtonRight)
        