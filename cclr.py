class cclr():
    
    def __init__(self):
        self.list = [(255, 0, 0),
         (0, 0, 255), 
         (0, 255, 0),
         (0, 0, 0),
         (0, 255, 255), 
         (255, 255, 0), 
         (255, 255, 102)]
        
        self.counter = 0
    
    def getnext(self):
        self.counter += 1
        self.counter = self.counter % len(self.list)

        return self.list[self.counter]

    def getErase(self):
        return (1,2,3)
    
    def getBack(self):
        return self.list[self.counter]
    
        
