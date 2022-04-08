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