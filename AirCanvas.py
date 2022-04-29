#@author: Swornim Chhetri
# This is the main page that shows all the things seen on the screen page, including the buttons

import cv2

from Canvas import Canvas
import HandDetector
import time
from clr import clr
import keyboard

# Getting the camera input and setting a constant height and width
camera = cv2.VideoCapture(0) 
camera.set(3,780)
camera.set(4,780)

# Creating a canvas object 
canvas = Canvas(camera)

detector = HandDetector.HandDetector() # The hand detector obejct
hand = detector.getHands() # The hand object from the hand detector

# This is for testing the frame rate. This is not used in screen but mostly for testing purpose
previous_time = 0

ccnow = clr.red.value # The current color

# Standard thickness
thick = 5
# Previous point initialized to 0,0
pp = [0,0]

# l is for straight line and rect is for rectangle
l = False
rect = False

f2 = False # for color changing screen.
t2 = False # for thickness changing screen.
l2 = True # for changing the drawing method screen.

while camera.isOpened():
    # Camera read returns a succes boolean and an image
    success, frame = camera.read()
       
    if not success:
        print("Ignoring empty camera frame.")
        # If loading a video, use 'break' instead of 'continue'
        continue
    
    # frameW is used for coordinate calucaltions.
    frameW = frame.shape[1]

    # This is done to make the image processing faster. Hand's process method works faster
    # when the video space is RGB
    frame.flags.writeable = False
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hand.process(frame)

    # Converting frames to BGR space again to make other processes faster
    # I am not exactly sure why this is faster but this was the way used in mediapipe's example
    frame.flags.writeable = True
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    # Getting the hand lankmarks
    lmList = detector.getLandmark(frame, results)

    # This bigger if statement controls the use of boxes in different screens
    # Because the camera frame is flipped it is important to flip the frame first before comparing the coordintates
    if results.multi_hand_landmarks:
        # This is for the color changing
        if f2:
            frame = cv2.flip(frame,1)
            # In each of the control statement a subsequent if is necessary to make sure that screen does not change
            # if the users did not select any color

            # Also in all of the color positions, if pinky is down then the color is changed and the color screen is set to false

            # For the position of green
            if (170 < lmList[8][1] < 210) and  (65 < lmList[8][2] < 105):  
                # Creates a black box around the hovered color for visual cue
                cv2.rectangle(frame, (frameW - 212, 63), (frameW-168, 107), clr.black.value)
                if detector.pinkyDown(lmList):
                    ccnow = clr.green.value
                    f2 = False
            # For the position of black
            elif (120 < lmList[8][1] < 160) and  (65 < lmList[8][2] < 105): 
                # Creates a black box around the hovered color for visual cue  
                cv2.rectangle(frame, (frameW - 162, 63), (frameW-118, 107), clr.black.value)
                if detector.pinkyDown(lmList):
                    ccnow = clr.black.value
                    f2 = False
            # For the position of cyan
            elif (70 < lmList[8][1] < 110) and  (65 < lmList[8][2] < 105):   
                # Creates a black box around the hovered color for visual cue
                cv2.rectangle(frame, (frameW - 112, 63), (frameW-68, 107), clr.black.value)
                if detector.pinkyDown(lmList):
                    ccnow = clr.cyan.value
                    f2 = False
            # For the position of yellow.
            elif (170 < lmList[8][1] < 210) and  (110 < lmList[8][2] < 150): 
                # Creates a black box around the hovered color for visual cue.   
                cv2.rectangle(frame, (frameW - 212, 108), (frameW-168, 152), clr.black.value)
                if detector.pinkyDown(lmList):
                    ccnow = clr.yellow.value
                    f2 = False
            # For the position of red
            elif (120 < lmList[8][1] < 160) and  (110 < lmList[8][2] < 150):    
                # Creates a black box around the hovered color for visual cue
                cv2.rectangle(frame, (frameW - 162, 108), (frameW-118, 152), clr.black.value)
                if detector.pinkyDown(lmList):
                    ccnow = clr.red.value
                    f2 = False
            # For the position of blue
            elif (70 < lmList[8][1] < 110) and  (110 < lmList[8][2] < 150):
                # Creates a black box around the hovered color for visual cue
                cv2.rectangle(frame, (frameW - 112, 108), (frameW-68, 152), clr.black.value)
                if detector.pinkyDown(lmList):
                    ccnow = clr.blue.value
                    f2 = False
            # Flip the frame again at the end
            frame = cv2.flip(frame,1)   
        
        # This is for changing thickness
        elif t2:
            # Flip the frame because the camera input is flipped
            frame = cv2.flip(frame,1)

            # In each of the control statement a subsequent if is necessary to make sure that screen does not change
            # if the users did not select any thickness

            # Also in all of the thickness values, if pinky is down then the thickness is changed and the thickness screen is set to false

            # 15 thickness
            if (40 < lmList[8][1] < 280) and (20 < lmList[8][2] < 260):
                # Creates a black box around the hovered color for visual cue
                cv2.rectangle(frame, (frameW - 282, 18), (frameW-38, 262), clr.black.value, 3)
                if detector.pinkyDown(lmList):
                    thick = 15
                    t2 = False
            # 10 thickness
            elif (290 < lmList[8][1] < 530) and (20 < lmList[8][2] < 260):
                # Creates a black box around the hovered color for visual cue
                cv2.rectangle(frame, (frameW - 532, 18), (frameW-288, 262), clr.black.value, 3)
                if detector.pinkyDown(lmList):
                    thick = 10
                    t2 = False
            # 5 thickness
            elif (540 < lmList[8][1] < 780) and (20 < lmList[8][2] < 260):
                # Creates a black box around the hovered color for visual cue
                cv2.rectangle(frame, (frameW - 782, 18), (frameW-538, 262), clr.black.value, 3)
                if detector.pinkyDown(lmList):
                    thick = 5
                    t2 = False
            # Flip the frame again at the end
            frame = cv2.flip(frame,1)

        # This is for the changing of shape type
        elif l2:
            frame = cv2.flip(frame,1)

            # In each of the control statement a subsequent if is necessary to make sure that screen does not change
            # if the users did not select any thickness

            # Also in all of the shape type, if pinky is down then the shape is changed and the shape screen is set to false
            
            # For the rectangle
            if (40 < lmList[8][1] < 280) and (20 < lmList[8][2] < 260):
                # Creates a black box around the hovered color for visual cue
                cv2.rectangle(frame, (frameW - 282, 18), (frameW-38, 262), clr.black.value, 3)
                if detector.pinkyDown(lmList):
                    l = False
                    rect = True
                    l2 = False
            # For the free draw
            elif (290 < lmList[8][1] < 530) and (20 < lmList[8][2] < 260):
                # Creates a black box around the hovered color for visual cue
                cv2.rectangle(frame, (frameW - 532, 18), (frameW-288, 262), clr.black.value, 3)
                if detector.pinkyDown(lmList):
                    l = False
                    rect = False
                    l2 = False
            # For the line
            elif (540 < lmList[8][1] < 780) and (20 < lmList[8][2] < 260):
                # Creates a black box around the hovered color for visual cue
                cv2.rectangle(frame, (frameW - 782, 18), (frameW-538, 262), clr.black.value, 3)
                if detector.pinkyDown(lmList):
                    l = True
                    rect = False
                    l2 = False
            # Flip the frame again at the end
            frame = cv2.flip(frame,1)

        # This is for the main screen.
        else:
            # If the user hovers over the clear screen button, then call clearText from detector
            if (20 < lmList[8][1] < 80) and  (20 < lmList[8][2] < 60):
                detector.clearText(canvas)
            # If the user hover over the color circle, set the color changing screen to True
            elif (120 < lmList[8][1] < 160) and  (20 < lmList[8][2] < 60):
                f2 = True if f2 == False else False
            # If the user hovers over the erase button.
            elif (440 < lmList[8][1] < 500) and  (20 < lmList[8][2] < 60):
                # Only call the erase function if the index finger was not on the erase button the last frame else just draw existing curves
                # This makes is so that erase button only erases once per button hover
                if not ((440 < pp[0] < 500) and  (20 < pp[1] < 60)):
                    detector.erase(canvas, lmList)
                else:
                    detector.draw(frame, canvas, ccnow, thick, lmList, l, rect)
            # If the user hovers over the thickness button, set the thickness changing screen to True
            elif (220 < lmList[8][1] < 300) and  (20 < lmList[8][2] < 60):
                t2 = True
            # If the user hover overs the shape button, set the shape changing screen to True
            elif (340 < lmList[8][1] < 420) and (20 < lmList[8][2] < 60):
                l2 = True
            else:
                # The call the draw method from the self wrote detector class
                detector.draw(frame, canvas, ccnow, thick, lmList, l, rect)

        # Save the current position of index as the previous positon. 8 is the index value in the hand landmark list    
        _, pp[0], pp[1] = lmList[8]


    #Flip the frame to ensure mirroring of camera input
    frame = cv2.flip(frame, 1)

    # If change color screen is true
    if f2:
        # Show the current color
        cv2.circle(frame, (frameW-140, 40),20, ccnow, cv2.FILLED)
        cv2.rectangle(frame, (frameW - 162, 18), (frameW-118, 62), clr.black.value)

        # Show all the changable colors
        cv2.circle(frame, (frameW-190, 85),20, clr.green.value, cv2.FILLED)
        cv2.circle(frame, (frameW-140, 85),20, clr.black.value, cv2.FILLED)
        cv2.circle(frame, (frameW-90, 85),20, clr.cyan.value, cv2.FILLED)
        cv2.circle(frame, (frameW-190, 130),20, clr.yellow.value, cv2.FILLED)
        cv2.circle(frame, (frameW-140, 130),20, clr.red.value, cv2.FILLED)
        cv2.circle(frame, (frameW-90, 130),20, clr.blue.value, cv2.FILLED)

        # Tip on how to use the screen
        cv2.rectangle(frame, (frameW - 830, 450), (frameW-20, 480), (200,200,200), cv2.FILLED)
        cv2.putText(frame, "Hover over with palm open to select and raise just the index to choose", (frameW-820, 470), 3, 0.6, clr.black.value, 1, 16, False)

    # If thickness changing screen is set to True  
    elif t2:
        # Show a example line with thickness 15
        cv2.rectangle(frame, (frameW - 280, 20), (frameW-40, 260), clr.red.value)
        cv2.line(frame, (frameW-260, 75), (frameW - 80, 220), ccnow, 15, cv2.LINE_AA)

        # Show a example line with thickness 10
        cv2.rectangle(frame, (frameW - 530, 20), (frameW-290, 260), clr.red.value)
        cv2.line(frame, (frameW-510, 75), (frameW - 330, 220), ccnow, 10, cv2.LINE_AA)

        # Show a example line with thickness 5
        cv2.rectangle(frame, (frameW - 780, 20), (frameW-540, 260), clr.red.value)
        cv2.line(frame, (frameW-760, 75), (frameW - 580, 220), ccnow, 5, cv2.LINE_AA)

        # Tip on how to use the screen
        cv2.rectangle(frame, (frameW - 830, 450), (frameW-20, 480), (200,200,200), cv2.FILLED)
        cv2.putText(frame, "Hover over with palm open to select and raise just the index to choose", (frameW-820, 470), 3, 0.6, clr.black.value, 1, 16, False)

    # If shape changing screen is set to True    
    elif l2:
        # Show a example of what rectangle looks like for visual cue. Users can draw this when the box is selected
        cv2.rectangle(frame, (frameW - 280, 20), (frameW-40, 260), clr.red.value)
        cv2.rectangle(frame, (frameW - 260, 60), (frameW-60, 220), ccnow, 5)
        cv2.putText(frame, "Rectangle", (frameW-260,50), 3, 1, (255,255,255), 1, 16, False)

        # Show a example of what free draw looks like for visual cue. Users can draw this when the box is selected
        cv2.rectangle(frame, (frameW - 530, 20), (frameW-290, 260), clr.red.value)
        cv2.line(frame, (frameW-510, 75), (frameW - 460, 200), ccnow, 5, cv2.LINE_AA) 
        cv2.line(frame, (frameW-460, 200), (frameW - 410, 90), ccnow, 5, cv2.LINE_AA)
        cv2.line(frame, (frameW-410, 90), (frameW - 360, 220), ccnow, 5, cv2.LINE_AA)
        cv2.putText(frame, "Free draw", (frameW-510,60), 3, 1, (255,255,255), 1, 16, False)
        
        # Show a example of what line looks like for visual cue. Users can draw this when the box is selected
        cv2.rectangle(frame, (frameW - 780, 20), (frameW-540, 260), clr.red.value)
        cv2.line(frame, (frameW-760, 75), (frameW - 580, 220), ccnow, 5, cv2.LINE_AA)
        cv2.putText(frame, "Line", (frameW-760,60), 3, 1, (255,255,255), 1, 16, False)

        # Tip on how to use the screen
        cv2.rectangle(frame, (frameW - 830, 450), (frameW, 480), (200,200,200), cv2.FILLED)
        cv2.putText(frame, "Hover over with palm open to select and raise just the index to choose", (frameW-820, 470), 4, 0.6, clr.black.value, 1, 16, False)

    # This is for the main screen
    else:
        # Show clear screen button
        cv2.rectangle(frame, (frameW - 80, 20), (frameW-20, 60), clr.black.value, cv2.FILLED)
        cv2.putText(frame, "Clear", (frameW-75,45), 0, 0.6, (255,255,255), 1, 16, False)
        
        # Show change color button with currently selected color
        cv2.circle(frame, (frameW-140, 40),20, ccnow, cv2.FILLED)
        # Show the erase button
        cv2.rectangle(frame, (frameW - 500, 20), (frameW-440, 60), clr.black.value, cv2.FILLED)
        cv2.putText(frame, "Erase", (frameW-495,45), 0, 0.6, (255,255,255), 1, 16, False)

        # Show the changing shape button with the current selected one on the box. Also changes the text cue on the top-left corner of the screen
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

        # show the thickness changing button with a example of currently selected thickness
        cv2.rectangle(frame, (frameW - 300, 20), (frameW-220, 60), clr.black.value)
        cv2.line(frame, (frameW-300, 40), (frameW - 220, 40), ccnow, thick)

        # Tip on how to use the screen
        cv2.rectangle(frame, (frameW - 830, 430), (frameW, 480), (200,200,200), cv2.FILLED)
        cv2.putText(frame, "To draw raise just the index finger; To stop drawing opem palm", (frameW-820, 450), 3, 0.6, clr.black.value, 1, 16, False)
        cv2.putText(frame, "Hover over with palm open to select the buttons", (frameW-820, 470), 3, 0.6, clr.black.value, 1, 16, False)

    
    # calucaltion of fps for testing purposes
    current_time = time.time()
    fps = 1/(current_time - previous_time)
    previous_time = current_time


    # Display the frames
    cv2.imshow('frame', frame)
    canvas.show()
    
    # Setting the quit button to c. If c is prssed then break out of the main loop
    # This is way cv2 uses the exit button. This waitKey is important to get the camera input working correct so could not
    # change this to keyboard.is_pressed()
    # IMPORTANT: This is case sensitive
    if cv2.waitKey(1) & 0xFF == ord('c'):
        break
    
    # If y is pressed then save the current workspace 
    if keyboard.is_pressed('y') or keyboard.is_pressed("Y"):
        detector.save()
    
    # If l is pressed then load the saved workspace
    if keyboard.is_pressed('l') or keyboard.is_pressed("L"):
        detector.load(lmList)

    # if s is pressed then save the whiteboard as an image
    if keyboard.is_pressed('s') or keyboard.is_pressed("S"):
        cv2.imwrite("saveFile.jpeg", canvas.can)

# release the camera resources and destroy the window
camera.release()
cv2.destroyAllWindows()