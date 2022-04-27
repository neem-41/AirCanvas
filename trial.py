import cv2
import numpy as np

can = np.zeros((740, 740, 3), dtype=np.uint8)
can.fill(255)

pts = np.array([[506, 249],
        [507, 256],
        [515, 266],
        [529, 270],
        [546, 270],
        [563, 262],
        [576, 250], 
        [588, 240], 
        [595, 228], 
        [602, 216], 
        [606, 206], 
        [613, 200]], dtype=np.int32)

cv2.polylines(can, [pts], False, (255,0,0), 5)
cv2.imshow('frame', can)


