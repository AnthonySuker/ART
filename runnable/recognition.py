import cv2 as cv
import json
import socket
import sys
import math
import pickle
import numpy as np

default_file = 'D:\\Documents\\UNI\\CSCI318\\ART\\Pics\\square.png'

src = cv.imread(default_file,cv.IMREAD_COLOR)

HOST = '127.0.0.1'
PORT = 65432
count = 0




def getDistance(l):
    x1,y1,x2,y2 = l[0],l[1],l[2],l[3]
    return math.sqrt((x2-x1)**2 + (y2-y1)**2)


####IMAGE DETECTOR####
#recieves cv::mat object
#detects its shape type by number of sides
#Sends to appropriate method
def detectImg(src):
    #decide which shape is detected by linking number of lines read to a function
    shapes ={
        1:'circle',
        3 : 'triangle',
        4 : 'square' ,
    }
    #create mats for use

    gray = cv.cvtColor(src,cv.COLOR_BGR2GRAY)
    dst = cv.Canny(gray,50,200,None,3)
    cdst = cv.cvtColor(dst,cv.COLOR_GRAY2BGR)
    lines = cv.HoughLinesP(dst,1, np.pi / 180, 50, None, 50, 10)

    


    try:
        if lines is None:
            try:
                gray = cv.blur(gray,(3,3))
                detected_circles = cv.HoughCircles(gray,cv.HOUGH_GRADIENT,1,20, param1=50,param2=30,minRadius=1,maxRadius=500)
                return("circle",detected_circles[0][2])
            except:
                return("circle", 0)
        else:
            print(len(lines))
            l = lines[0][0]
            return(shapes[len(lines)],getDistance(l))
    except:
        print("returned unknown")
        return("Unknown",0.0)


def colourAtCenter(img):
    h,w,c = img.shape
    print( h, w, c)

    h = int(h/2)
    w = int(w/2)
    print( h, w, c)
    print
    return img[h][w]


#recieves binary data of a cv::mat object
#unpickles said data
#saves image 
#sends to detect img
def translateData(data):
    global count
    baseURL = "D:\\Documents\\UNI\\CSCI318\\ART\\Imgs\\"
    url = baseURL+"img_"+str(count)+".png"
    img = pickle.loads(data)
    cv.imwrite(url,img)
    return img


def jsonCreator(data,colour):
    print(data)
    print(colour)

    temp = {}
    try:
        temp["type"] = data[0]
        temp["size"] = int(data[1])
    except:
        temp["type"] = "unknown"
        temp["size"] = 0 
    temp["red"] = int(colour[0])
    temp["green"] = int(colour[1])
    temp["blue"] = int(colour[2])
    print(temp)
    jsonData = json.dumps(temp)
    return jsonData


def handler(data):
    global count
    count += 1

    img = translateData(data)
    data = detectImg(img)
    colour = colourAtCenter(img)
    jsonData = pickle.dumps(jsonCreator(data,colour))
    return jsonData

#SERVER FUNCTION
def startServer():
    print("starting server.....",end='')
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        print("started")
        with conn:
            print('Connected by'+ str(addr))
            while True:
                data = conn.recv(786597)
                if not data:
                    break
                conn.sendall(handler(data))

startServer()