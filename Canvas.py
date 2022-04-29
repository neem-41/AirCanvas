# @author: Swornim Chhetri
# This is the Canvas class that creates a canvas page depending on the height and the width of 
# of the camera input.

# importing necessary packages
import cv2
import numpy as np

class Canvas():

    # Constructor for Canvas.
    # Usage Canvas(camera: cv2 camera object)
    def __init__(self, camera):
        self.camera = camera
        self.height = int(self.camera.get(4))
        self.width = int(self.camera.get(3))
        self.can = np.zeros((self.height, self.width, 3), dtype=np.uint8) # this is the canvas body.
        self.can.fill(255)
    
    # method to show the canvas on the screen.
    def show(self):
        cv2.imshow('canvas', self.can)
    
    # method to close the canvas window
    def close():
        cv2.destroyAllWindows()

    # clear method to reset all the pixels to white.
    def clear(self):
        self.can.fill(255)
        
