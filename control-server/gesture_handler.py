import enum
from typing import Dict
from executor_utils import Executor
import numpy as np

REPLY_OK = "OK"
PREFIX_OPEN_APP_PROMPT = "Open "
PREFIX_CLOSE_APP_PROMPT = "Close "
SUFFIX_PROMPT = " ?"
PREFIX_OPENED_APP_MESSAGE = "Opened "
PREFIX_CLOSED_APP_MESSAGE = "Closed "
OPEN_APP_CANCEL_MESSAGE = "Cancelled"
UNAVAILABLE_APP = "No app configured to open"
MOUSE_POINTER_ACTIVE = "Mouse pointer control activated"
MOUSE_POINTER_INACTIVE = "Mouse pointer control deactivated"

DEFAULT_APP = "App"

class AppStatus(enum.Enum):
    inactive = 0
    await_user_prompt = 1
    open = 2
    mouse_pointer_active = 3

class HandKeypoint:
    def __init__(self, x, y, z=None):
        self.x = x
        self.y = y
        self.z = z

class GestureHandler:
    def __init__(self, sensitivity, exec_endpoint, mouse_movement_sensitivity, mouse_click_sensitivity):
        #Initialise landmarks
        self.__initialise_landmarks()
        #General settings
        self.exec = Executor(base_endpoint=exec_endpoint)
        self.sensitivity = sensitivity
        self.app = DEFAULT_APP
        self.app_id = None
        self.app_status = AppStatus.inactive
        self.gesture = None
        self.frame_counter = 0
        #Settings to control mouse
        self.mouse_movement_sensitivity = mouse_movement_sensitivity
        self.mouse_click_sensitivity = mouse_click_sensitivity
        self.mouse_pointer_tracking = None
        self.mouse_allow_click = False
        self.mouse_static_counter = 0

    def __initialise_landmarks(self):
        self.landmarks = {}
        for i in range(20):
            self.landmarks[i] = None
        self.N_landmarks = 0
        self.landmark_h = 0
        self.landmark_w = 0    

    """
    Check if thumb is raised or not
    """
    def __isThumbRaised(self):
        fixedPoint_x = self.landmarks[2].x
        return self.landmarks[3].x > fixedPoint_x and \
               self.landmarks[4].x > fixedPoint_x   
    
    """
    Check if thumb is down or not
    """
    def __isThumbDown(self):
        fixedPoint_y = self.landmarks[2].y
        return self.landmarks[3].y < fixedPoint_y and \
               self.landmarks[4].y < fixedPoint_y     
    
    """
    Check if first finger is raised or not
    """
    def __isFirstFingerRaised(self):
        fixedPoint_y = self.landmarks[5].y
        return self.landmarks[6].y < fixedPoint_y and \
               self.landmarks[7].y < fixedPoint_y and \
               self.landmarks[8].y < fixedPoint_y 

    """
    Check if second finger is raised or not
    """
    def __isSecondFingerRaised(self):
        fixedPoint_y = self.landmarks[9].y
        return self.landmarks[10].y < fixedPoint_y and \
               self.landmarks[11].y < fixedPoint_y and \
               self.landmarks[12].y < fixedPoint_y 

    """
    Check if third finger is raised or not
    """
    def __isThirdFingerRaised(self):
        fixedPoint_y = self.landmarks[13].y
        return self.landmarks[14].y < fixedPoint_y and \
               self.landmarks[15].y < fixedPoint_y and \
               self.landmarks[16].y < fixedPoint_y

    """
    Check if fourth finger is raised or not
    """
    def __isFourthFingerRaised(self):
        fixedPoint_y = self.landmarks[17].y
        return self.landmarks[18].y < fixedPoint_y and \
               self.landmarks[19].y < fixedPoint_y and \
               self.landmarks[20].y < fixedPoint_y

    """
    Check if thumb lies to the left or right of the remaining fingers
    """
    def __computeHandOrientation(self):
        fixedPoint_x = self.landmarks[5].x
        if self.landmarks[3].x < fixedPoint_x and \
           self.landmarks[4].x < fixedPoint_x:
           return 'left'
        else:
           return 'right'     

    """
    Check if user sent a thumbs up or thumbs down
    """
    def __parseAppConsentGesture(self):
        if not self.__isFirstFingerRaised() and \
           not self.__isSecondFingerRaised() and \
           not self.__isThirdFingerRaised() and \
           not self.__isFourthFingerRaised():
           thumb_tip_y = self.landmarks[4].y
           first_finger_knuckle_y = self.landmarks[6].y 
           if thumb_tip_y < first_finger_knuckle_y:
               return 'Yes'
           else:
               return 'No' 
        else:
            return 'Ignore'                      

    """
    Count number of raised fingers in gesture for app open
    """
    def __countRaisedFingers(self):
        numFingersRaised = 0
        if self.__isThumbRaised():
            numFingersRaised += 1
        if self.__isFirstFingerRaised():
            numFingersRaised += 1
        if self.__isSecondFingerRaised():
            numFingersRaised += 1
        if self.__isThirdFingerRaised():
            numFingersRaised += 1
        if self.__isFourthFingerRaised():
            numFingersRaised += 1
        return numFingersRaised                    

    """
    Check if user sent gesture to close currently open app
    """
    def __isAppCloseGesture(self):
        numFingersRaised = self.__countRaisedFingers()
        return numFingersRaised == 5

    def __resetGestureTracking(self):
        self.gesture = None
        self.frame_counter = 0

    def __resetAppTracking(self):
        self.app = DEFAULT_APP
        self.app_id = None
    
    """
    Check if user sent gesture to get control of mouse pointer
    """
    def __isMousePointerGesture(self):
        numFingersRaised = self.__countRaisedFingers()
        return numFingersRaised == 1 and self.__isFirstFingerRaised()
    
    def __isRightClickGesture(self):
        numFingersRaised = self.__countRaisedFingers()
        return numFingersRaised == 2 and self.__isFirstFingerRaised() and self.__isSecondFingerRaised()

    def __getFirstFingerTipPosition(self):
        return [self.landmarks[8].x, self.landmarks[8].y]

    """
    Parse client message and produce dictionary of landmarks
    """    
    def __parseClientMessage(self, client_msg: str) -> Dict:
        landmark_list = client_msg.split("|")
        del landmark_list[0]
        dims = landmark_list[0]
        info = dims.split(",")
        self.landmark_h = float(info[1])
        self.landmark_w = float(info[2])
        del landmark_list[0]
        self.N_landmarks = len(landmark_list)
        if self.N_landmarks == 21:    
            for landmark in landmark_list:
                info = landmark.split(",")
                self.landmarks[int(info[0])] = HandKeypoint(x = float(info[1]), \
                                                            y = float(info[2]))

    """
    Parse landmarks and update state of object
    """
    def updateLandmarks(self, client_msg: str) -> str:
        self.__parseClientMessage(client_msg)

        if self.N_landmarks < 21:
            self.__resetGestureTracking()
            return REPLY_OK

        reply = REPLY_OK

        if self.app_status == AppStatus.inactive:
            current_gesture = self.__countRaisedFingers()
            if self.gesture == None or self.gesture != current_gesture:
                self.gesture = current_gesture
                self.frame_counter = 1
            
            else:
                self.frame_counter += 1
                
                if self.frame_counter == self.sensitivity:
                    app_id, app_name = self.exec.getAppDetails(self.gesture)
                    if app_name == "":
                        reply = UNAVAILABLE_APP
                        self.__resetGestureTracking()
                    
                    else:
                        self.app_id = app_id
                        self.app = app_name    
                        self.app_status = AppStatus.await_user_prompt
                        self.__resetGestureTracking()
                        reply = PREFIX_OPEN_APP_PROMPT+self.app+SUFFIX_PROMPT      
        
        elif self.app_status == AppStatus.await_user_prompt:
            current_gesture = self.__parseAppConsentGesture()
            
            if current_gesture == 'Ignore':
                self.__resetGestureTracking()
            
            else:    
                if self.gesture == None or self.gesture != current_gesture:
                    self.gesture = current_gesture
                    self.frame_counter = 1
                
                else:
                    self.frame_counter += 1
                    
                    if self.frame_counter == self.sensitivity:
                        if current_gesture == 'Yes':
                            self.exec.openApp(self.app_id)
                            self.app_status = AppStatus.open
                            reply = PREFIX_OPENED_APP_MESSAGE+self.app
                        
                        else:
                            self.app_status = AppStatus.inactive
                            reply = OPEN_APP_CANCEL_MESSAGE
                        self.__resetGestureTracking()
        
        elif self.app_status == AppStatus.mouse_pointer_active:
            if self.__isMousePointerGesture():
                self.__resetGestureTracking()
                new_position = self.__getFirstFingerTipPosition()
                dist_moved = np.linalg.norm(np.asarray(new_position) - np.asarray(self.mouse_pointer_tracking))
                if dist_moved > self.mouse_movement_sensitivity:
                    self.mouse_pointer_tracking = new_position
                    self.mouse_static_counter = 0
                    self.exec.moveMouse(self.landmark_w - new_position[0], new_position[1])
                    self.mouse_allow_click = True
                
                else:
                    self.mouse_static_counter += 1

                if self.mouse_static_counter == self.mouse_click_sensitivity and self.mouse_allow_click:
                    self.mouse_allow_click = False
                    self.mouse_static_counter = 0
                    current_position = self.mouse_pointer_tracking
                    self.exec.leftClickMouse(self.landmark_w - current_position[0], current_position[1])
            
            elif self.__isRightClickGesture():
                self.gesture = 2
                self.frame_counter += 1
                if self.frame_counter == self.sensitivity:
                    current_position = self.mouse_pointer_tracking
                    self.exec.rightClickMouse(self.landmark_w - current_position[0], current_position[1])
                    self.__resetGestureTracking()
                    self.app_status = AppStatus.open
            
            else:
                self.app_status = AppStatus.open
                reply = MOUSE_POINTER_INACTIVE
                self.mouse_static_counter = 0
                self.mouse_allow_click = False
                self.__resetGestureTracking()
        
        else:
            if self.__isMousePointerGesture():
                self.app_status = AppStatus.mouse_pointer_active
                reply = MOUSE_POINTER_ACTIVE
                self.mouse_pointer_tracking = self.__getFirstFingerTipPosition()
                self.__resetGestureTracking()
            
            elif self.__isAppCloseGesture():
                self.gesture = 5
                self.frame_counter += 1
                if self.frame_counter == self.sensitivity:
                    self.exec.closeApp(self.app_id)
                    self.app_status = AppStatus.inactive
                    self.__resetGestureTracking()
                    reply = PREFIX_CLOSED_APP_MESSAGE+self.app
                    self.__resetAppTracking()          
            
            else:
                self.__resetGestureTracking()
        
        return reply        
