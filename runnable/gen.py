import numpy as np
import cv2 as cv
import math
import random as rand
import keyboard as key
import socket 
import pickle
import json

import threading
import time

HOST = '127.0.0.1'
PORT = 65432
imgSize = 512

hist = []
results = []
newData = False
data = ""


#TODO ART Algorithm
#TODO Data logging
#TODO Recieve Response
#TODO save information


def addConsoleData(s):
    global newData,data
    if not newData:
        newData = True
        data = s
    else:
        data = data +"\n"
        data = data + s



def generateRect(size, colour):
    img = np.zeros((imgSize,imgSize,3), np.uint8)
    anchor = imgSize - size
    anchorTL = int(anchor / 2)
    anchorBR = int(imgSize - anchorTL)

    cv.rectangle(img,(anchorTL,anchorTL),(anchorBR,anchorBR),(colour),-1)
    return img

def generateCirc(size,colour):
    img = np.zeros((imgSize,imgSize,3), np.uint8)
    anchor = int(imgSize/2)
    #convert size to radius instead of diameter
    size = int(size / 2)
    cv.circle(img,(anchor,anchor),size,(colour),-1)
    return img

def generateTri(size,colour):
    img = np.zeros((imgSize,imgSize,3), np.uint8)
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
    return img


drawFunc ={
        0: generateRect,
        1: generateCirc,
        2: generateTri,
    }
    
class shape:
    #red, green, blue, size, type
    def __init__(self,r,g,b,s,t):
        self.r, self.g, self.b, self.s, self.t = r,g,b,s,t
        if(t == 0):
            self.name = "rectangle"
        elif(t==1):
            self.name = "Circle"
        else:
            self.name = "Triangle"

    def distFrom(self,r,g,b):
        return math.sqrt( (self.r-r)**2 + (self.g-g)**2 + (self.b-b)**2 ) 
    
    def drawToImg(self):
        colour = (self.r,self.g,self.b)
        return drawFunc[self.t](self.s,colour)

    def colourDist(self,c):
        distance = math.sqrt(math.pow(c.r - self.r,2) +
        math.pow(c.g-self.g,2) +
        math.power(c.b-self.b,2) * 1.0)
        return distance
    
    def getColour(self):
        colour = (self.r,self.g,self.b)
        return colour

    def getStr(self):
        s = '"type": %s , "size": %i, "red": %i, "green": %i, "blue": %i' %(self.name,self.s,self.r,self.g,self.b)
        return s


def getImg(i):
    obj = hist[i]
    return obj.drawToImg()



    

def exportNew():
    ts = time.gmtime()
    tm = time.strftime('%X',ts)

    addConsoleData(tm+" Generating... Sending Image")
    first()
    draw()
    data = pickle.dumps(img)
    return data

def first():
    img = np.zeros((imgSize,imgSize,3), np.uint8)
    r = rand.randint(0,255)
    g = rand.randint(0,255)
    b = rand.randint(0,255)
    s = rand.randint(0,500)
    colour = (r,g,b)
    shape_type = rand.randint(0,2)
    t = shape(r,g,b,s,shape_type)
    hist.append(t)



#basically redo this to use shape.dist to compare colours in '3d space'
#it doesnt work anyway so no real worries in deleting all of it
#generate k shapes 
#create art algo using shapes.dist for colour and idk for size
#maybe art them seperately
def generate():
    k = 4
    candidates = []
    choice = None
    max_distance = 0
        
    #generate k candidates
    candidates.clear()
    for i in range(0,k+1):
        red = rand.randint(0,255)
        green = rand.randint(0,255)
        blue = rand.randint(0,255)
        size = rand.randint(0,500)
        shape_type = rand.randint(0,2)
        cand = shape(red,green,blue,size,shape_type)
        candidates.append(cand)

    #iterate through history and determine choice
    #goes through and finds every candidates closest 'real' point
    #chooses the candidate that is furthest from its closest
    for c in candidates:
        min_distance = 100000
        for h in hist:
            d = c.distFrom(h.getColour()[0],h.getColour()[1],h.getColour()[2])
            if d < min_distance:
                min_distance = d
        if min_distance > max_distance:
            choice = c
            max_distance = min_distance
    hist.append(choice)

def getDiff(a, b):
    if a == b:
        return 100.0
    try:
        return (abs(a - b) / b) * 100.0
    except ZeroDivisionError:
        return 0

#recieves shape object and json string, verifys information
def verifyData(shape,jdata):
    global results
    print(jdata)
    info = json.loads(jdata)
    print(info)
    print(shape.r,shape.g,shape.b)
    print(info["red"],info["green"],info["blue"])

    #get colour correctness
    red_diff = getDiff(info["red"], shape.r)
    green_diff = getDiff(info["green"], shape.g)
    blue_diff =  getDiff(info["blue"], shape.b)

    col_dif = (red_diff + green_diff + blue_diff)/3

    print('DOING SIZE DIFF')
    print(info["size"],shape.s)
    size_dif = getDiff(info["size"],shape.s)

    t = 0
    if (info["type"]=="square"):
        t = 0
    elif(info["type"]=="circle"):
        t=1
    elif(info["type"]=="triangle"):
        t=2
    else:
        t= -1

    shape_correct = False
    if(t == shape.t):
        shape_correct = True

    temp = {}
    temp["col_dif"] = col_dif
    temp["size_dif"] = size_dif
    temp["shape"] = shape_correct

    print(temp)

    results.append(temp)
    print(len(results))




                    

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def connect():
    try:
        s.connect((HOST,PORT))
        return True
    except:
        return False

#generate all cases and then send them all

def startUp(iterations,perc):
    rhist = []
    hist.clear()
    results.clear()
    first()
    for i in range(1,iterations):
        generate()

    #try:
    for i in hist:
        img = i.drawToImg()
        img_data = pickle.dumps(img)
        s.sendall(img_data)
        info_data = s.recv(16384)
        info_data = pickle.loads(info_data)
        verifyData(i,info_data)
        rhist.append(i.getStr())


    print("RESULTS")
    print(len(results))

    avg_shape = 0
    avg_size = 0
    avg_col = 0
    for i in results:
        if i['shape'] == True:
            avg_shape = avg_shape+1
        
        avg_size = avg_size +i['size_dif']
        avg_col = avg_col + i['col_dif']
    avg_shape = avg_shape / iterations*100
    avg_size = avg_size / iterations
    avg_col = avg_col / iterations



    
    return(avg_shape,avg_size,avg_col,rhist,results)






print('linked')

