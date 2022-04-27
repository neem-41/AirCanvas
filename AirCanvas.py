import numpy as np
import cv2
from collections import deque
from Canvas import Canvas
import HandDetector
import time
import math
from clr import clr
import enum
import cclr
import keyboard

camera = cv2.VideoCapture(0) 
camera.set(3,780)
camera.set(4,780)

canvas = Canvas(camera)

detector = HandDetector.HandDetector()
hand = detector.getHands()

previous_time = 0
kernel = np.ones((5, 5), np.uint8)
stop = False

cnow = cclr.cclr()
ccnow = cnow.getnext()

# standard thickness
thick = 5
# previous point initialized to 0,0
pp = [0,0]

l = False
rect = False

f2 = False # for color changing
t2 = False # for thickness changing
l2 = True # for changing the drawing method

while camera.isOpened():
    success, image = camera.read()
       
    if not success:
        print("Ignoring empty camera frame.")
        # If loading a video, use 'break' instead of 'continue'.
        continue
    
    # Capture frames of the video
    sommething, frame = camera.read()
    frameW = frame.shape[1]

    
    frame.flags.writeable = False
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hand.process(frame)

    frame.flags.writeable = True
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    #cv2.putText(frame, str(int(fps)), (20,50), 1, 3, (0,255,0), 2)
    lmList = detector.getLandmark(frame, results)

    if results.multi_hand_landmarks:
        # This is for the color changing
        if f2:
            frame = cv2.flip(frame,1)
            #if (420 < lmList[8][1] < 460) and  (120 < lmList[8][2] < 160):    
            #    cv2.rectangle(frame, (frameW - 462, 118), (frameW-418, 162), clr.black.value)
            if (170 < lmList[8][1] < 210) and  (65 < lmList[8][2] < 105):    
                cv2.rectangle(frame, (frameW - 212, 63), (frameW-168, 107), clr.black.value)
                if detector.pinkyDown(lmList):
                    ccnow = clr.green.value
                    f2 = False
            elif (120 < lmList[8][1] < 160) and  (65 < lmList[8][2] < 105):    
                cv2.rectangle(frame, (frameW - 162, 63), (frameW-118, 107), clr.black.value)
                if detector.pinkyDown(lmList):
                    ccnow = clr.black.value
                    f2 = False
            elif (70 < lmList[8][1] < 110) and  (65 < lmList[8][2] < 105):    
                cv2.rectangle(frame, (frameW - 112, 63), (frameW-68, 107), clr.black.value)
                if detector.pinkyDown(lmList):
                    ccnow = clr.cyan.value
                    f2 = False
            elif (170 < lmList[8][1] < 210) and  (110 < lmList[8][2] < 150):    
                cv2.rectangle(frame, (frameW - 212, 108), (frameW-168, 152), clr.black.value)
                if detector.pinkyDown(lmList):
                    ccnow = clr.yellow.value
                    f2 = False
            elif (120 < lmList[8][1] < 160) and  (110 < lmList[8][2] < 150):    
                cv2.rectangle(frame, (frameW - 162, 108), (frameW-118, 152), clr.black.value)
                if detector.pinkyDown(lmList):
                    ccnow = clr.red.value
                    f2 = False
            elif (70 < lmList[8][1] < 110) and  (110 < lmList[8][2] < 150):
                cv2.rectangle(frame, (frameW - 112, 108), (frameW-68, 152), clr.black.value)
                if detector.pinkyDown(lmList):
                    ccnow = clr.blue.value
                    f2 = False
            frame = cv2.flip(frame,1)   
        elif t2:
            frame = cv2.flip(frame,1)

            # 15 thickness
            if (40 < lmList[8][1] < 280) and (20 < lmList[8][2] < 260):
                cv2.rectangle(frame, (frameW - 282, 18), (frameW-38, 262), clr.black.value, 3)
                if detector.pinkyDown(lmList):
                    thick = 15
                    t2 = False
            # 10 thickness
            elif (290 < lmList[8][1] < 530) and (20 < lmList[8][2] < 260):
                cv2.rectangle(frame, (frameW - 532, 18), (frameW-288, 262), clr.black.value, 3)
                if detector.pinkyDown(lmList):
                    thick = 10
                    t2 = False
            # 5 thickness
            elif (540 < lmList[8][1] < 780) and (20 < lmList[8][2] < 260):
                cv2.rectangle(frame, (frameW - 782, 18), (frameW-538, 262), clr.black.value, 3)
                if detector.pinkyDown(lmList):
                    thick = 5
                    t2 = False
            frame = cv2.flip(frame,1)
        # This is for the changing of drawing material.
        elif l2:
            frame = cv2.flip(frame,1)
            # For the rectangle.
            if (40 < lmList[8][1] < 280) and (20 < lmList[8][2] < 260):
                cv2.rectangle(frame, (frameW - 282, 18), (frameW-38, 262), clr.black.value, 3)
                if detector.pinkyDown(lmList):
                    l = False
                    rect = True
                    l2 = False
            # For the free draw
            elif (290 < lmList[8][1] < 530) and (20 < lmList[8][2] < 260):
                cv2.rectangle(frame, (frameW - 532, 18), (frameW-288, 262), clr.black.value, 3)
                if detector.pinkyDown(lmList):
                    l = False
                    rect = False
                    l2 = False
            # For the line
            elif (540 < lmList[8][1] < 780) and (20 < lmList[8][2] < 260):
                cv2.rectangle(frame, (frameW - 782, 18), (frameW-538, 262), clr.black.value, 3)
                if detector.pinkyDown(lmList):
                    l = True
                    rect = False
                    l2 = False
            frame = cv2.flip(frame,1)
        # for all the other stuff
        else:
            if (20 < lmList[8][1] < 80) and  (20 < lmList[8][2] < 60):
                detector.clearText(canvas)
            elif (120 < lmList[8][1] < 160) and  (20 < lmList[8][2] < 60):
                f2 = True if f2 == False else False
                
            elif (440 < lmList[8][1] < 500) and  (20 < lmList[8][2] < 60):
                if not ((440 < pp[0] < 500) and  (20 < pp[1] < 60)):
                    detector.erase(canvas, lmList)
                else:
                    detector.draw(frame, canvas, ccnow, thick, lmList, l, rect)
            elif (220 < lmList[8][1] < 300) and  (20 < lmList[8][2] < 60):
                t2 = True
            elif (340 < lmList[8][1] < 420) and (20 < lmList[8][2] < 60):
                l2 = True
            else:
                # The draw method is on the HandDetector class that I wrote.
                detector.draw(frame, canvas, ccnow, thick, lmList, l, rect)
            
        _, pp[0], pp[1] = lmList[8]

    #detector.checkButton(frame)

    #Flip the frame to make the hand tracking easier
    frame = cv2.flip(frame, 1)

    if f2:
        cv2.circle(frame, (frameW-140, 40),20, ccnow, cv2.FILLED)
        cv2.rectangle(frame, (frameW - 162, 18), (frameW-118, 62), clr.black.value)

        cv2.circle(frame, (frameW-190, 85),20, clr.green.value, cv2.FILLED)
        cv2.circle(frame, (frameW-140, 85),20, clr.black.value, cv2.FILLED)
        cv2.circle(frame, (frameW-90, 85),20, clr.cyan.value, cv2.FILLED)
        cv2.circle(frame, (frameW-190, 130),20, clr.yellow.value, cv2.FILLED)
        cv2.circle(frame, (frameW-140, 130),20, clr.red.value, cv2.FILLED)
        cv2.circle(frame, (frameW-90, 130),20, clr.blue.value, cv2.FILLED)

        cv2.rectangle(frame, (frameW - 830, 450), (frameW-20, 480), (200,200,200), cv2.FILLED)
        cv2.putText(frame, "Hover over with palm open to select and raise just the index to choose", (frameW-820, 470), 3, 0.6, clr.black.value, 1, 16, False)
        
    elif t2:
        cv2.rectangle(frame, (frameW - 280, 20), (frameW-40, 260), clr.red.value)
        cv2.line(frame, (frameW-260, 75), (frameW - 80, 220), ccnow, 15, cv2.LINE_AA)

        cv2.rectangle(frame, (frameW - 530, 20), (frameW-290, 260), clr.red.value)
        cv2.line(frame, (frameW-510, 75), (frameW - 330, 220), ccnow, 10, cv2.LINE_AA)

        cv2.rectangle(frame, (frameW - 780, 20), (frameW-540, 260), clr.red.value)
        cv2.line(frame, (frameW-760, 75), (frameW - 580, 220), ccnow, 5, cv2.LINE_AA)

        cv2.rectangle(frame, (frameW - 830, 450), (frameW-20, 480), (200,200,200), cv2.FILLED)
        cv2.putText(frame, "Hover over with palm open to select and raise just the index to choose", (frameW-820, 470), 3, 0.6, clr.black.value, 1, 16, False)
        
    elif l2:
        cv2.rectangle(frame, (frameW - 280, 20), (frameW-40, 260), clr.red.value)
        cv2.rectangle(frame, (frameW - 260, 60), (frameW-60, 220), ccnow, 5)
        cv2.putText(frame, "Rectangle", (frameW-260,50), 3, 1, (255,255,255), 1, 16, False)

        cv2.rectangle(frame, (frameW - 530, 20), (frameW-290, 260), clr.red.value)
        cv2.line(frame, (frameW-510, 75), (frameW - 460, 200), ccnow, 5, cv2.LINE_AA) 
        cv2.line(frame, (frameW-460, 200), (frameW - 410, 90), ccnow, 5, cv2.LINE_AA)
        cv2.line(frame, (frameW-410, 90), (frameW - 360, 220), ccnow, 5, cv2.LINE_AA)
        cv2.putText(frame, "Free draw", (frameW-510,60), 3, 1, (255,255,255), 1, 16, False)
        
        cv2.rectangle(frame, (frameW - 780, 20), (frameW-540, 260), clr.red.value)
        cv2.line(frame, (frameW-760, 75), (frameW - 580, 220), ccnow, 5, cv2.LINE_AA)
        cv2.putText(frame, "Line", (frameW-760,60), 3, 1, (255,255,255), 1, 16, False)

        cv2.rectangle(frame, (frameW - 830, 450), (frameW, 480), (200,200,200), cv2.FILLED)
        cv2.putText(frame, "Hover over with palm open to select and raise just the index to choose", (frameW-820, 470), 4, 0.6, clr.black.value, 1, 16, False)

    else:
        # Clear screen
        cv2.rectangle(frame, (frameW - 80, 20), (frameW-20, 60), clr.black.value, cv2.FILLED)
        cv2.putText(frame, "Clear", (frameW-75,45), 0, 0.6, (255,255,255), 1, 16, False)
        # Change color
        cv2.circle(frame, (frameW-140, 40),20, ccnow, cv2.FILLED)
        # Erase
        #cv2.rectangle(frame, (frameW - 660, 20), (frameW-620, 60), clr.cyan.value, cv2.FILLED)
        cv2.rectangle(frame, (frameW - 500, 20), (frameW-440, 60), clr.black.value, cv2.FILLED)
        cv2.putText(frame, "Erase", (frameW-495,45), 0, 0.6, (255,255,255), 1, 16, False)

        # Changing drawing material
        cv2.rectangle(frame, (frameW - 420, 20), (frameW-340, 60), clr.black.value)
        if l:
            cv2.line(frame, (frameW-400, 25), (frameW - 360, 55), ccnow, 2, cv2.LINE_AA)
            cv2.putText(frame, "On Line Mode", (frameW-820, 20), 3, 0.8, (255,255,255), 2, 16, False)
        elif rect:
            cv2.rectangle(frame, (frameW-400, 25), (frameW - 360, 55), ccnow, 2)
            cv2.putText(frame, "On Rectangle Mode", (frameW-820, 20), 3, 0.8, (255,255,255), 2, 16, False)
        else:
            cv2.line(frame, (frameW-410, 25), (frameW - 390, 50), ccnow, 2, cv2.LINE_AA)
            cv2.line(frame, (frameW-390, 50), (frameW - 370, 30), ccnow, 2, cv2.LINE_AA)
            cv2.line(frame, (frameW-370, 30), (frameW - 350, 50), ccnow, 2, cv2.LINE_AA)
            cv2.putText(frame, "On Free Mode", (frameW-820, 20), 3, 0.8, (255,255,255), 2, 16, False)

        #thickness
        cv2.rectangle(frame, (frameW - 300, 20), (frameW-220, 60), clr.black.value)
        cv2.line(frame, (frameW-300, 40), (frameW - 220, 40), ccnow, thick)

        
        cv2.rectangle(frame, (frameW - 830, 430), (frameW, 480), (200,200,200), cv2.FILLED)
        cv2.putText(frame, "To draw raise just the index finger; To stop drawing opem palm", (frameW-820, 450), 3, 0.6, clr.black.value, 1, 16, False)
        cv2.putText(frame, "Hover over with palm open to select the buttons", (frameW-820, 470), 3, 0.6, clr.black.value, 1, 16, False)

    

    current_time = time.time()
    fps = 1/(current_time - previous_time)
    #fps = 1/ (time.time() - p)
    previous_time = current_time


    # Display the frames
    cv2.imshow('frame', frame)
    canvas.show()
    
    # Setting the quit button to c
    if cv2.waitKey(1) & 0xFF == ord('c'):
        break
    
    if keyboard.is_pressed('y'):
        detector.save()
    
    if keyboard.is_pressed('l'):
        detector.load(lmList)

    if keyboard.is_pressed('s'):
        cv2.imwrite("saveFile.jpeg", canvas.can)

    
camera.release()
cv2.destroyAllWindows()