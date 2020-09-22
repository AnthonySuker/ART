import numpy as np
import cv2 as cv
import math
import random as rand
import keyboard as key
import socket 
import pickle

HOST = '127.0.0.1'
PORT = 65432
imgSize = 512
img = np.zeros((imgSize,imgSize,3), np.uint8)
hist = []
SERVER_STATE = FALSE


#TODO ART Algorithm
#TODO Data logging
#TODO Recieve Response
#TODO save information






def generateRect(img,size, colour):
    anchor = imgSize - size
    anchorTL = int(anchor / 2)
    anchorBR = int(imgSize - anchorTL)

    cv.rectangle(img,(anchorTL,anchorTL),(anchorBR,anchorBR),(colour),-1)

def generateCirc(img,size,colour):
    anchor = int(imgSize/2)
    #convert size to radius instead of diameter
    size = int(size / 2)
    cv.circle(img,(anchor,anchor),size,(colour),-1)

def generateTri(img,size,colour):
    #get anchors for x axis
    anchor = imgSize - size
    anchorXBL = int(anchor / 2)
    anchorXBR = int(anchorXBL + size)
    anchorXTOP = int(imgSize/2)

    #anchors for y axis
    height = int((size * math.sqrt(3))/2)
    anchor = imgSize - height
    anchorYTOP = int(anchor / 2)
    anchorYBOT = int(anchorYTOP+height)

    pt1 = (anchorXTOP,anchorYTOP)
    pt2 = (anchorXBL,anchorYBOT)
    pt3 = (anchorXBR,anchorYBOT)

    pts = np.array([pt1,pt2,pt3])
    cv.drawContours(img,[pts],0,colour,-1)


drawFunc ={
        0: generateRect,
        1: generateCirc,
        2: generateTri,
    }
    
class shape:
    #red, green, blue, size, type
    def __init__(self,r,g,b,s,t):
        self.r, self.g, self.b, self.s, self.t = r,g,b,s,t

    def distFrom(self,x,y,z):
        return math.sqrt( (self.x-x)**2 + (self.y-y)**2 + (self.z-z)**2 ) 
    
    def drawToImg(self):
        colour = (self.r,self.g,self.b)
        drawFunc[self.t](img,self.s,colour)





def draw():
    obj = hist[-1]
    obj.drawToImg()


    

def exportNew():
    first()
    draw()
    #cv.imshow("img",img)
    #cv.waitKey(0)
    data = pickle.dumps(img)
    #print(len(data))
    return data

def first():
    img.fill(0)
    r = rand.randint(0,255)
    g = rand.randint(0,255)
    b = rand.randint(0,255)
    s = rand.randint(0,500)
    colour = (r,g,b)
    opt = rand.randint(0,2)
    t = shape(r,g,b,s,opt)
    hist.append(t)



#basically redo this to use shape.dist to compare colours in '3d space'
#it doesnt work anyway so no real worries in deleting all of it
#generate k shapes 
#create art algo using shapes.dist for colour and idk for size
#maybe art them seperately
def generate():
    k = 4
    candidates = []
    choice = 0
        

    for i in range(0,2):
        candidates.clear()
        for j in range(0,k):
            
            t = rand.randint(0,255)
            candidates.append(t)
        
        for c in candidates:
            dist = 1000
            topDist = 0
            for x in col[i]:
                d = abs(c-x)
                if d < dist:
                    dist = d

            if(dist > topDist):
                topDist = dist
                choice = c
                    







#generateRect(img,500,(255,255,0))
#generateCirc(img,500,(255,0,0))
#generateTri(img,500,(255,0,255))


# first()
# showRecent()

# pimg = pickle.dumps(img)
# upimg = pickle.loads(pimg)


# cv.imshow('image',upimg)
# cv.waitKey(0)



# while True:
#     try:
#         if key.is_pressed('space'):
#             first()
#             showRecent()


#             cv.imshow('image',upimg)
#             cv.waitKey(0)
#         elif key.is_pressed('q'):
#             break
#     except:
#         print("key pressed")

def START_SERVER():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            while SERVER_STATE:
                data = conn.recv(1024)
                if not data:
                    break
                print("recieved request:",data)
                conn.sendall(exportNew())



cv.destroyAllWindows()




