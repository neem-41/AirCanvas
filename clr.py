#@author: Swornim Chhetri
# This is color class that takes color input as BGR instead of RBG.
# It was important to make this because the image is converted into BGR on the main page.
import enum

class clr(enum.Enum):
    blue = (255, 0, 0)
    red = (0, 0, 255)
    green = (0, 255, 0)
    black = (0, 0, 0)
    yellow = (0, 255, 255)
    cyan = (255, 255, 0)
    skyBlue = (255, 255, 102)