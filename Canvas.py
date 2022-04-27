import cv2
import numpy as np

class Canvas():
    def __init__(self, camera):
        self.camera = camera
        self.height = int(self.camera.get(4))
        self.width = int(self.camera.get(3))
        self.can = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        self.previous = self.can.copy()
        self.can.fill(255)
    
    def show(self):
        cv2.imshow('canvas', self.can)
    
    def close():
        cv2.destroyAllWindows()

    def clear(self):
        self.can = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        self.can.fill(255)

    def setPrevious(self, containter):
        self.previous = containter
        
