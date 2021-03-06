# @author: Swornim Chhetri
# This is HandDetector class where the methods to draw, erase, etc are made.

import mediapipe as mp
import cv2
import csv

class HandDetector():
    # Constructor for the Hand Detector Class
    def __init__(self):
        self.handpipe = mp.solutions.hands
        self.hands = self.handpipe.Hands(max_num_hands=1, model_complexity=0, min_detection_confidence=0.5, min_tracking_confidence=0.5)
        self.drawpipe = mp.solutions.drawing_utils
        self.drawingstyles = mp.solutions.drawing_styles
        self.queue = [] # for the canvas
        self.queue2 = [] # for the frame
        self.color = [] # for the color
        self.thickness = [] # for the thickness of the line
        self.rec = [] # for the rectangle.
        self.current_color = (0,0,255)

    # Method to return the hand location
    def getHands(self):
        return self.hands

    # Method to get the handpipe
    def getHandPipe(self):
        return self.handpipe

    # The draw method to draw on the screen.
    # Usage: draw(frame: camera input, canvas: canvas object, color: clr enum, list: landmark list, line: boolean, rectangle: boolean)
    def draw(self, frame, canvas, color, thickness, list, line, rectangle):
        lmlist = list

        # this creates the yellow circle around the index finger.        
        cv2.circle(frame, (lmlist[8][1], lmlist[8][2]), 10, (0,255,255))
        
        # Only draw if the pinky finger is down.
        if (self.pinkyDown(lmlist)):

            # get the () [null imitation] values in teh coordinates 
            empty = [i for i,value in enumerate(self.queue2) if value == ()]
            # if it is line or rectangle then we only want two points at a section so remove the last drawn point
            # if it is line or rectangle.
            if line or rectangle:
                if len(empty) == 0:
                    # if there are only two lines in the queue.
                    if len(self.queue) == 2:
                        self.queue.pop(-1)
                        self.queue2.pop(-1)
                        self.color.pop(-1)
                        self.thickness.pop(-1)
                        self.rec.pop(-1)
                        canvas.clear()
                else:
                    # if there are more than two points after the last drawn section.
                    if len(self.queue) == empty[-1] + 3:
                        self.queue.pop(-1)
                        self.queue2.pop(-1)
                        self.color.pop(-1)
                        self.thickness.pop(-1)
                        self.rec.pop(-1)
                        canvas.clear()

            # add the new point to the coordinate system.
            self.queue.append((frame.shape[1] - lmlist[8][1], lmlist[8][2]))
            self.queue2.append((lmlist[8][1], lmlist[8][2]))
            self.color.append(color)
            self.thickness.append(thickness)
            self.rec.append(rectangle)
        else:
            # append a blank tuple if pinky is up.
            if (self.queue2):
                if self.queue2[-1] != ():
                    self.queue2.append(())
                    self.queue.append(())
                    self.color.append(())
                    self.thickness.append(())
                    self.rec.append(())


        length = len(self.queue)
        # if there are more than just one point on the queue
        if (length > 1):
            # Draw all the points. This is needed because frame gets refreshed everytime
            # so it is necessary to draw all the points everytime.
            for i in range(length -1):
                # checking queue2 is full here to avoid error after queue is cleared.
                if self.queue2:
                    if self.queue2[i] and self.queue2[i+1]:
                        # if rectangle is true then draw a rectangle else draw a line.
                        if self.rec[i]:
                            cv2.rectangle(frame, self.queue2[i], self.queue2[i+1], (self.color[i]), self.thickness[i])
                            cv2.rectangle(canvas.can, self.queue[i], self.queue[i+1], (self.color[i]), self.thickness[i])
                        else:
                            cv2.line(frame, self.queue2[i], self.queue2[i+1], (self.color[i]), self.thickness[i], cv2.LINE_AA)
                            cv2.line(canvas.can, self.queue[i], self.queue[i+1], (self.color[i]), self.thickness[i], cv2.LINE_AA)

    def pinkyDown(self, list):
        # comparing the y coordinate of tip of pinky and the mid to test if pinky is up.
        return list[20][2] - list[18][2] > 0

    # clear all the text and colors if the clear button is called.
    def clearText(self, canvas):
        self.queue2 = []
        self.queue = []
        self.color = []
        self.thickness = []
        self.rec = []
        canvas.clear()

    def getLandmark(self, frame, results):
        lmlist = []
        self.frame = frame
        # check if there is hand in the frame. results will have all the landmarks if a hand is detected.
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                #creating a id for each point in the landmark
                for id, lm in enumerate(hand_landmarks.landmark):
                    h, w, c = frame.shape
                    cx, cy = int(lm.x*w), int(lm.y*h)
                    # Adding the dots of hands to a list. 8 is index finger tip.
                    lmlist.append([id,cx,cy])
                    
        return lmlist


    # The erase method to erase the last drawn line.
    # () on the queue means that the user has stopped drawing (pinky up). I will refer to this as a pause.
    def erase(self, canvas, list):
        empty = [i for i,value in enumerate(self.queue2) if value == ()]
        # if there is only one line drawn
        if (len(empty) == 0):
            self.clearText(canvas)
        else:
            # if the person is still drawing erase everything after the last pause
            if self.pinkyDown(list):
                lidex = empty[-1]
            # if the person is not drawing
            else:
                # if only one pause and not drawing erase everything
                if (len(empty) == 1):
                    lidex = 0
                # if more than one pause erase everything after the second last pause - this deletes the last line
                else:
                    lidex = empty[-2]

            canvas.clear()
            self.queue = self.queue[0:lidex]
            self.queue2 = self.queue2[0:lidex]
            self.color = self.color[0:lidex]
            self.thickness = self.thickness[0:lidex]
            self.rec = self.rec[0:lidex]
            
            # without this if there is only one pause and the person is not drawing
            # the lists will have () as the starting point. This will not affect the program 
            # but is a waste of memory
            if (lidex != 0):
                self.queue.append(())
                self.queue2.append(())
                self.color.append(())
                self.thickness.append(())
                self.rec.append(())
    
    # This is the save method that saves the current working space.
    def save(self):
        # opent he file and save the values setting ! as the delimiter.
        with open('save.dat', 'w') as file:
            file.write('!'.join(str(k) for k in self.queue) + '\n')
            file.write('!'.join(str(k) for k in self.queue2) + '\n')
            file.write('!'.join(str(k) for k in self.color) + '\n')
            file.write('!'.join(str(k) for k in self.thickness) + '\n')
            file.write('!'.join(str(k) for k in self.rec) + '\n')
    
    # This is the load method that loads the saved working space.
    def load(self, list):
        # If the user is writing when this method is called a null is added to the coordinate system
        # this way the laoded values are not joined with the drawing the user is making.
        if list:
            if self.pinkyDown(list):
                self.queue.append(())
                self.queue2.append(())
                self.color.append(())
                self.thickness.append(())
                self.rec.append(())

        # Open the save file and add the values to the coordinate system.  
        with open('save.dat', 'r') as file:
            reader = csv.reader(file, delimiter = '!')
            for count, row in enumerate(reader):
                for element in row:
                    if count == 0:
                        self.queue.append(eval(element))
                    elif count == 1:
                        self.queue2.append(eval(element))
                    elif count == 2:
                        self.color.append(eval(element))
                    elif count == 3:
                        self.thickness.append(eval(element))
                    elif count == 4:
                        self.rec.append(eval(element))
                            

                
                    
                


        

        
