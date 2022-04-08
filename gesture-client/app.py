"""
Client-side module for hand gesture control
"""
import os
from collections import OrderedDict
import cv2
import mediapipe as mp
from utils import ServerChannel
from dotenv import load_dotenv

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

MSG_FEED_ACTIVE = ""
MSG_IGNORE_EMPTY_FRAME = ""

def capture_webcam():
    cap = cv2.VideoCapture(0)
    print(MSG_FEED_ACTIVE)
    return cap

def initialise_mp_hands(m_c,m_d_c,m_t_c):
    return mp_hands.Hands(model_complexity=m_c,min_detection_confidence=m_d_c,min_tracking_confidence=m_t_c)

def clientProcess(cap, hands, server_channel: ServerChannel):
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print(MSG_IGNORE_EMPTY_FRAME)
            # If loading a video, use 'break' instead of 'continue'.
            continue

        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(image)

        # Draw the hand annotations on the image.
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    image,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style())

        # Flip the image horizontally for a selfie-view display.
        cv2.imshow('MediaPipe Hands', cv2.flip(image, 1))
        
        #collect landmarks
        landmarks = OrderedDict()
        imageHeight, imageWidth, _ = image.shape
        landmarks['dims'] = [imageHeight, imageWidth]
        if results.multi_hand_landmarks != None:
            handTypes = []
            for hand in results.multi_handedness:
                handType=hand.classification[0].label
                handTypes.append(handType)
            #invert due to guaranteed incorrect classification by mediapipe
            for i in range(len(handTypes)):
                if handTypes[i] == 'Right':
                    handTypes[i] = 'Left'
                else:
                    handTypes[i] = 'Right'
            for handLandmarks, handType in zip(results.multi_hand_landmarks,handTypes):
                count = 0
                landmarks[str(handType)] = {}
                for point in mp_hands.HandLandmark:
                    count+=1
                    normalizedLandmark = handLandmarks.landmark[point]
                    pixelCoordinatesLandmark = mp_drawing._normalized_to_pixel_coordinates(normalizedLandmark.x, normalizedLandmark.y, imageWidth, imageHeight)
                    landmarks[str(handType)][str(point)] = pixelCoordinatesLandmark  

        #send landmarks to server
        server_channel.sendLandmarks(landmarks)

        #press escape key to close program
        if cv2.waitKey(5) & 0xFF == 27:
            break

    #release feed
    cap.release()
    #kill communications with server
    server_channel.killAgent()

if __name__ == '__main__':
    load_dotenv()
    MSG_FEED_ACTIVE = os.getenv('MSG_FEED_ACTIVE')
    MSG_IGNORE_EMPTY_FRAME = os.getenv('MSG_IGNORE_EMPTY_FRAME')
    cap = capture_webcam()
    hands = initialise_mp_hands(int(os.getenv('HANDS_MODEL_COMPLEXITY')), \
                                float(os.getenv('HANDS_MIN_DETECTION_CONFIDENCE')), \
                                float(os.getenv('HANDS_MIN_TRACKING_CONFIDENCE')))
    server_channel = ServerChannel(host=os.getenv('CONTROL_SERVER_HOST'), \
                                   port=int(os.getenv('CONTROL_SERVER_PORT')), \
                                   autoconnect=int(os.getenv('CONTROL_SERVER_AUTOCONNECT')))
    print("Server channel created. Connection status =",server_channel.connected)
    clientProcess(cap, hands, server_channel)
