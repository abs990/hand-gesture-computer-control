import enum
from typing import Dict
from executor_utils import Executor
from hand_pose import Hand
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
        self.left_hand = None
        self.right_hand = None
        self.landmark_h = 0
        self.landmark_w = 0
    """
    Check if user sent a thumbs up or thumbs down
    """
    def __parseAppConsentGesture(self):
        if not self.__isRightHandAvailable():
           return 'Ignore' 
        elif not self.right_hand.isFirstFingerRaised() and \
           not self.right_hand.isSecondFingerRaised() and \
           not self.right_hand.isThirdFingerRaised() and \
           not self.right_hand.isFourthFingerRaised():
           thumb_tip_y = self.right_hand.landmarks[4].y
           first_finger_knuckle_y = self.right_hand.landmarks[6].y 
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
        count = 0
        if self.__isRightHandAvailable():
            count += self.right_hand.countRaisedFingers()
        if self.__isLeftHandAvailable():
            count += self.left_hand.countRaisedFingers()
        return count                  

    """
    Check if user sent gesture to close currently open app - cross hands at wrists like an x
    """

    def __unit_vector(self, vector):
        return vector / np.linalg.norm(vector)

    def __isAppCloseGesture(self):

        if self.right_hand == None or \
            self.left_hand == None or \
            self.right_hand.N_landmarks < 21 or \
            self.left_hand.N_landmarks < 21:
            return False

        else:
            right_wrist_pos = self.right_hand.landmarks[0]
            right_wrist_pos = np.array([right_wrist_pos.x, right_wrist_pos.y])
            left_wrist_pos = self.left_hand.landmarks[0]
            left_wrist_pos = np.array([left_wrist_pos.x, left_wrist_pos.y])
            right_middle_finger_base_pos = self.right_hand.landmarks[9]
            right_middle_finger_base_pos = np.array([right_middle_finger_base_pos.x, right_middle_finger_base_pos.y])
            left_middle_finger_base_pos = self.left_hand.landmarks[9]
            left_middle_finger_base_pos = np.array([left_middle_finger_base_pos.x, left_middle_finger_base_pos.y])

            if right_middle_finger_base_pos[0] < left_middle_finger_base_pos[0]:
                return False
            
            wrist_diff = np.linalg.norm(right_wrist_pos - left_wrist_pos)
            if wrist_diff > 100:
                return False

            right_hand_vec = right_middle_finger_base_pos - right_wrist_pos
            left_hand_vec = left_middle_finger_base_pos - left_wrist_pos
            right_u = self.__unit_vector(right_hand_vec)
            left_u = self.__unit_vector(left_hand_vec)

            angle =  np.degrees(np.arccos(np.clip(np.dot(right_u, left_u), -1.0, 1.0)))

            if angle < 60 or angle > 100:
                return False

            return True

    def __resetGestureTracking(self):
        self.gesture = None
        self.frame_counter = 0

    def __resetAppTracking(self):
        self.app = DEFAULT_APP
        self.app_id = None
    
    """
    Check if user sent gesture to get control of mouse pointer
    """
    def __isRightHandAvailable(self):
        return self.right_hand != None and self.right_hand.N_landmarks == 21

    def __isLeftHandAvailable(self):
        return self.left_hand != None and self.left_hand.N_landmarks == 21 

    def __isMousePointerGesture(self):
        if not self.__isRightHandAvailable():
            return False
        numFingersRaised = self.right_hand.countRaisedFingers()
        return numFingersRaised == 1 and self.right_hand.isFirstFingerRaised()
    
    def __isRightClickGesture(self):
        if not self.__isRightHandAvailable():
            return False
        numFingersRaised = self.right_hand.countRaisedFingers()
        return numFingersRaised == 2 and self.right_hand.isFirstFingerRaised() and self.right_hand.isSecondFingerRaised()

    def __getRightFirstFingerTipPosition(self):
        return [self.right_hand.landmarks[8].x, self.right_hand.landmarks[8].y]

    """
    Special gestures
    """

    def __isLeftHandThumbRight(self):
        if not self.__isLeftHandAvailable():
            return False

        if self.left_hand.isFirstFingerRaised() or \
           self.left_hand.isSecondFingerRaised() or \
           self.left_hand.isThirdFingerRaised() or \
           self.left_hand.isFourthFingerRaised():
           return False 

        left_thumb_tip_x = self.left_hand.landmarks[4].x
        left_first_finger_base_x = self.left_hand.landmarks[5].x

        return left_thumb_tip_x < left_first_finger_base_x

    def __isRightHandThumbLeft(self):
        if not self.__isRightHandAvailable():
            return False

        if self.right_hand.isFirstFingerRaised() or \
           self.right_hand.isSecondFingerRaised() or \
           self.right_hand.isThirdFingerRaised() or \
           self.right_hand.isFourthFingerRaised():
           return False 

        right_thumb_tip_x = self.right_hand.landmarks[4].x
        right_first_finger_base_x = self.right_hand.landmarks[5].x

        return right_thumb_tip_x > right_first_finger_base_x

    def __isHandLShape(self, hand_type):
        if hand_type=='Right':
            if not self.__isRightHandAvailable():
                return False
            hand = self.right_hand
        
        if hand_type=='Left':
            if not self.__isLeftHandAvailable():
                return False
            hand = self.left_hand

        if hand.isSecondFingerRaised() or \
           hand.isThirdFingerRaised() or \
           hand.isFourthFingerRaised():
           return False

        if not hand.isThumbRaised() or \
           not hand.isFirstFingerRaised():
           return False

        thumb_base = hand.landmarks[1]
        thumb_base = np.array([thumb_base.x, thumb_base.y])
        thumb_tip = hand.landmarks[4]
        thumb_tip = np.array([thumb_tip.x, thumb_tip.y])
        first_finger_base = hand.landmarks[5]
        first_finger_base = np.array([first_finger_base.x, first_finger_base.y])
        first_finger_tip = hand.landmarks[8]
        first_finger_tip = np.array([first_finger_tip.x, first_finger_tip.y])

        f1 = thumb_tip - thumb_base
        f2 = first_finger_tip - first_finger_base

        f1_u = self.__unit_vector(f1)
        f2_u = self.__unit_vector(f2)

        angle =  np.degrees(np.arccos(np.clip(np.dot(f1_u, f2_u), -1.0, 1.0)))

        return angle >= 60

    def __isRightHandLShape(self):
        return self.__isHandLShape('Right')

    def __isLeftHandLShape(self):
        return self.__isHandLShape('Left')

    def __isBothHandsLShape(self):
        return self.__isRightHandLShape() and self.__isLeftHandLShape()

    """
    Parse client message and produce dictionary of landmarks
    """    
    def __parseClientMessage(self, client_msg: str) -> Dict:
        self.right_hand = None
        self.left_hand = None
        landmark_list = client_msg.split("|")
        del landmark_list[0]
        dims = landmark_list[0]
        info = dims.split(",")
        self.landmark_h = float(info[1])
        self.landmark_w = float(info[2])
        del landmark_list[0]
        current_hand = None
        current_landmarks = {}
        N_landmarks = {}
        for landmark in landmark_list:
            if landmark in ['Right', 'Left']:
                current_hand = landmark
                current_landmarks[current_hand] = [0]*21
                N_landmarks[current_hand] = 0
            else:
                info = landmark.split(",")
                current_landmarks[current_hand][int(info[0])] = HandKeypoint(x = float(info[1]), \
                                                                            y = float(info[2]))
                N_landmarks[current_hand] += 1
        if 'Right' in N_landmarks:
            hand_type = 'Right'
            self.right_hand = Hand(hand_type,current_landmarks[hand_type],N_landmarks[hand_type])
        if 'Left' in N_landmarks:
            hand_type = 'Left'
            self.left_hand = Hand(hand_type,current_landmarks[hand_type],N_landmarks[hand_type])

    """
    Parse landmarks and update state of object
    """
    def updateLandmarks(self, client_msg: str) -> str:
        self.__parseClientMessage(client_msg)

        #right hand is necessary to control the system
        #if self.right_hand == None or self.right_hand.N_landmarks < 21:
        #    self.__resetGestureTracking()
        #   return REPLY_OK
        if not self.__isRightHandAvailable() and not self.__isLeftHandAvailable():
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
                new_position = self.__getRightFirstFingerTipPosition()
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
                self.mouse_pointer_tracking = self.__getRightFirstFingerTipPosition()
                self.__resetGestureTracking()
            
            else: 
                if self.__isAppCloseGesture():
                    current_gesture = 11
                elif self.__isLeftHandThumbRight():
                    current_gesture = 12
                elif self.__isRightHandThumbLeft():
                    current_gesture = 13
                elif self.__isBothHandsLShape():
                    current_gesture = 15
                elif self.__isRightHandLShape():
                    current_gesture = 14
                else:
                    current_gesture = self.__countRaisedFingers()

                if self.gesture == None:
                    self.gesture = current_gesture    
                    self.frame_counter = 1
                elif self.gesture != current_gesture:
                    self.__resetGestureTracking()
                else:
                    self.frame_counter += 1
                
                if self.frame_counter == self.sensitivity:
                    if self.__isAppCloseGesture():
                        self.exec.closeApp(self.app_id)
                        self.app_status = AppStatus.inactive
                        self.__resetGestureTracking()
                        reply = PREFIX_CLOSED_APP_MESSAGE+self.app
                        self.__resetAppTracking()          
                    else:
                        self.exec.triggerSpecialGesture(self.app_id, self.gesture)

                    self.__resetGestureTracking()
        
        return reply        
