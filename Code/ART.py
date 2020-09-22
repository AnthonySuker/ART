import sys
import random as rand
import math

ties = 0

class point:
    def __init__(self, x, y):
        self.X = x
        self.Y = y
    
    def distance(self, p):
        dx = self.X - p.X
        dy = self.Y - p.Y
        return math.hypot(dx,dy)

class blackzone:
    minX,minY,maxX,maxY = 0,0,0,0
    def __init__(self,p):
        self.Size = p * 1000

    def newZone(self):
        maxRange = 100 - self.Size

        self.minX = rand.uniform(0,maxRange)
        self.minY = rand.uniform(0,maxRange)
        self.maxX = self.minX + self.Size
        self.maxY = self.minY + self.Size

        #print("Blackzone values: ", (self.minX, self.maxX, self.minY, self.maxY))

    def intersects(self, p):
        return p.X >= self.minX and p.X <= self.maxX and p.Y >= self.minY and p.Y <= self.maxY


        

class RTClass:
    
    hits = 0

    def createPoint(self):
        x = rand.uniform(0,100)
        y = rand.uniform(0,100)
        p = point(x,y)
        return p

    def increment(self):
        self.hits += 1
    
    def decrement(self):
        self.hits -=1

    def getHits(self):
        return self.hits

    
class ARTClass(RTClass):
    tests = []
    def reset(self):
        self.tests.clear()
        #print("NEW SETTT")

    def addFirstPoint(self, p):
        self.tests.append(p)

    def createPoint(self):
            
        k = 4
        candidates = []
        choice = 0
        topDist = 0

        for i in range(0,k):
            x = rand.uniform(0,100)
            y = rand.uniform(0,100)
            p = point(x,y)
            candidates.append(p)

    #run through every candidate and compare distances to all valid tests
    #choose candidate with longest distance to be added to valid test list
        distToFurthestNeighbour = 0

    #ROB
    #Changed this bit up a bit, it now looks for the closest test case for each candidate
    #And then picks the candidate with the furthest closest test case
        for c in candidates:
            closestNeighbour = 100000  #Just needed a max value
            for x in self.tests:
                dist = c.distance(x)
                if(dist < closestNeighbour):
                    closestNeighbour = dist
            if(closestNeighbour > distToFurthestNeighbour):
                distToFurthestNeighbour = closestNeighbour
                choice = c        
        
        self.tests.append(choice)
        return choice



failrate = float(input("Please enter a number between 0 & 1 for the failure rate: "))
bzone = blackzone(failrate)
      


ART = ARTClass()
RT = RTClass()

def run():
    global ties
    bzone.newZone()
    ART.reset()
    artFail = False
    rtFail = False
    endloop = False
    nTests = 0
    first = True
    while True:
        
        if first:
            first = False
            nTests += 1
            p = RT.createPoint()
            ART.addFirstPoint(p)
            artFail = bzone.intersects(p)
            rtFail = bzone.intersects(p)
        else:
            nTests += 1
            p = ART.createPoint()
            artFail = bzone.intersects(p)
            p = RT.createPoint()
            rtFail = bzone.intersects(p)
        
        print("Case %d: "%(nTests), end='')

        if(artFail):
            endloop = True
            ART.increment()
            print("ART - HIT   \t")
        else:
            print("ART - MISSED\t", end='')

        
        if(rtFail):
            endloop = True
            RT.increment()
            print("RT - HIT")
        else:
            print("RT - MISSED")

        if artFail and rtFail:
            ART.decrement()
            RT.decrement()
            ties += 1
        
        if endloop:
            break


        
numTests = int(input("Please enter the number of competitions: "))
for i in range(1,numTests+1):
    print("\nTEST #",i)
    run()

print("\n\nCompetitions Complete")
print("%d Tests have been completed; ART failed: %d \t RT failed: %d \tTies: %d"%(numTests,ART.getHits(),RT.getHits(),ties))
    



