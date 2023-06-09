import cv2 as cv
import mediapipe as mp
import time


class handDetector():
    def __init__(self, static_image_mode=False,max_num_hands=2,model_complexity=1,min_detection_confidence=0.5,min_tracking_confidence=0.5):
        self.static_image_mode= static_image_mode
        self.max_num_hands= max_num_hands
        self.model_complexity= 1
        self.min_detection_confidence= 0.5
        self.min_tracking_confidence=0.5
        self.mpHands= mp.solutions.hands
        self.hands= self.mpHands.Hands(self.static_image_mode, self.max_num_hands, self.model_complexity, self.min_detection_confidence, self.min_tracking_confidence)
        self.mpDraw= mp.solutions.drawing_utils
        self.tipIds= [4,8, 12, 16, 20]
    
    def FindHands(self, img, draw=True):
        imgRGB= cv.cvtColor(img, cv.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        #print(results.multi_hand_landmarks)
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img
            
    def findPosition(self,img, handNo=0, draw=True):
        self.lmList= []
        if self.results.multi_hand_landmarks:
            myHand= self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                h, w, c= img.shape
                cx, cy = int(lm.x*w), int(lm.y*h)
                self.lmList.append([id, cx, cy])
                if draw:
                    cv.circle(img, (cx, cy), 15, (255,0,255), cv.FILLED)
        return self.lmList


    def fingersUp(self):
        fingers= []
        if self.lmList[self.tipIds[0]][1] < self.lmList[self.tipIds[0]-1][1]:
                fingers.append(1)
        else:
            fingers.append(0)
        for id in range (1,5):
            if self.lmList[self.tipIds[id]][2] < self.lmList[self.tipIds[id]-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        return fingers



def main():
    pTime= 0 
    cTime= 0
    cap=cv.VideoCapture(0)
    detector= handDetector()

    while True:
        success, img= cap.read()
        img= detector.FindHands(img)
        lmList= detector.findPosition(img)
        if(len(lmList)!= 0):
            print(lmList[4])
        cTime= time.time()
        fps= 1/(cTime-pTime)
        pTime= cTime

        cv.putText(img, str(int(fps)), (10,70), cv.FONT_HERSHEY_PLAIN, 3, (255,0,255), 3)
        cv.imshow('Image', img)
        cv.waitKey(1)



if __name__== "__main__":
    main()