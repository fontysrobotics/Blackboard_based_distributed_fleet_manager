class Battery:
    def __init__(self, level, capacity, chargintTime):
        self.level = level
        self.capacity = capacity
        self.chargintTime = chargintTime

    def getVolt(self):
        return 10

    def getAmps(self):
        return ((self.level * self.capacity) / 100)
    

    def updateLevel(self,amps):
        self.level = self.level - ((100 * amps)/self.capacity)
        print('BatLevel task done:',self.level)
