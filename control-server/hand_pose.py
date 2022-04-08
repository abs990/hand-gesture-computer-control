class Hand:
    def __init__(self, hand_type, landmarks, N_landmarks):
        self.hand_type = hand_type
        self.landmarks = landmarks
        self.N_landmarks = N_landmarks

    """
    Check if thumb is raised or not
    """
    def isThumbRaised(self):
        fixedPoint_x = self.landmarks[2].x
        if self.hand_type == 'Right':
            return self.landmarks[3].x > fixedPoint_x and \
                self.landmarks[4].x > fixedPoint_x
        else:
            return self.landmarks[3].x < fixedPoint_x and \
                self.landmarks[4].x < fixedPoint_x               
    
    """
    Check if thumb is down or not
    """
    def isThumbDown(self):
        fixedPoint_y = self.landmarks[2].y
        return self.landmarks[3].y < fixedPoint_y and \
               self.landmarks[4].y < fixedPoint_y     
    
    """
    Check if first finger is raised or not
    """
    def isFirstFingerRaised(self):
        fixedPoint_y = self.landmarks[5].y
        return self.landmarks[6].y < fixedPoint_y and \
               self.landmarks[7].y < fixedPoint_y and \
               self.landmarks[8].y < fixedPoint_y 

    """
    Check if second finger is raised or not
    """
    def isSecondFingerRaised(self):
        fixedPoint_y = self.landmarks[9].y
        return self.landmarks[10].y < fixedPoint_y and \
               self.landmarks[11].y < fixedPoint_y and \
               self.landmarks[12].y < fixedPoint_y 

    """
    Check if third finger is raised or not
    """
    def isThirdFingerRaised(self):
        fixedPoint_y = self.landmarks[13].y
        return self.landmarks[14].y < fixedPoint_y and \
               self.landmarks[15].y < fixedPoint_y and \
               self.landmarks[16].y < fixedPoint_y

    """
    Check if fourth finger is raised or not
    """
    def isFourthFingerRaised(self):
        fixedPoint_y = self.landmarks[17].y
        return self.landmarks[18].y < fixedPoint_y and \
               self.landmarks[19].y < fixedPoint_y and \
               self.landmarks[20].y < fixedPoint_y

    def computeHandOrientation(self):
        fixedPoint_x = self.landmarks[5].x
        if self.landmarks[3].x < fixedPoint_x and \
           self.landmarks[4].x < fixedPoint_x:
           return 'left'
        else:
           return 'right'

    def countRaisedFingers(self):
        numFingersRaised = 0
        if self.isThumbRaised():
            numFingersRaised += 1
        if self.isFirstFingerRaised():
            numFingersRaised += 1
        if self.isSecondFingerRaised():
            numFingersRaised += 1
        if self.isThirdFingerRaised():
            numFingersRaised += 1
        if self.isFourthFingerRaised():
            numFingersRaised += 1
        return numFingersRaised