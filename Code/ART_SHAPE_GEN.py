import numpy as np
import cv2 as cv
import math
import random as rand
import keyboard as key
import socket 
import pickle

from threading import Thread
import time

HOST = '127.0.0.1'
PORT = 65432
imgSize = 512
img = np.zeros((imgSize,imgSize,3), np.uint8)
hist = []
stop_threads = False


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
                    



def START_SERVER(stop):
    global SERVER_STATE
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                print("recieved request:",data)
                conn.sendall(exportNew())
                if stop():
                    cv.destroyAllWindows()
                    break






## START GUI


from tkinter import filedialog
import tkinter as tk

window = tk.Tk()
window.title("ART Image Generator")
folder_path = tk.StringVar()
folder_path.set("File Save Location")

started = False

def updateConsole(text):
    global txt_console
    txt_console.configure(state="normal")
    txt_console.insert(tk.INSERT,text+'\n')
    txt_console.configure(state="disabled")


##FRAMES##
frm_top = tk.Frame(
    master = window,
)
frm_center = tk.Frame(
    master = window
)
frm_tests = tk.Frame(
    master = window   
)
frm_loc = tk.Frame(
    master=window,
    pady=10
)
frm_bot = tk.Frame(
    master = window,
)

frm_top.pack()
frm_center.pack(expand=True, anchor='w', fill='none')
frm_tests.pack()
frm_loc.pack(expand=False, anchor='w', fill='none')
frm_bot.pack()


## <TOP FRAME CONTENTS> 

lbl_status_blog = tk.Label(
    master = frm_top,
    text='Server Status: '
    )

lbl_status_actual = tk.Label(
    master = frm_top,
    text='OFFLINE',
    fg = 'red'
    )

lbl_status_blog.grid(row = 0, column = 0, padx=15)
lbl_status_actual.grid(row = 0, column = 1,padx=15)

## </TOP FRAME CONTENTS> 




## <CENTER FRAME CONTENTS>
saveImgVar = tk.IntVar()
saveJsonVar = tk.IntVar()
startBtnVar = tk.StringVar()
startBtnVar.set("Start")
tk.Checkbutton(
    master = frm_center,
    text = 'Save Generated Images',
    variable = saveImgVar
).grid(sticky='w',row = 0, column=0, padx=15)

saveJsonVar = 0
tk.Checkbutton(
    master = frm_center,
    text = 'Save Test Result Json',
    variable = saveJsonVar
).grid(sticky='e',row = 0, column=1, padx=15)




t1 = Thread(target = START_SERVER, args=(lambda : stop_threads, ))
t1.setDaemon(True)

def start_button():
    global started, btn_start, lbl_status_actual, SERVER_STATE
    started = not started
    if started:
        startBtnVar.set('Stop')
        lbl_status_actual.config(
            text = "ONLINE",
            fg = 'green'
        )
        updateConsole("Started")
        
        stop_threads = False
        t1.start()

    else:
        startBtnVar.set('Start')
        lbl_status_actual.config(
            text = "OFFLINE",
            fg = 'red'
        )
        updateConsole("Stopped")
        time.sleep(1)
        stop_threads = True
        t1.join()
    

    

btn_start = tk.Button(
    master = frm_tests,
    textvariable = startBtnVar,
    command=start_button
).grid(row = 0,column=0)

tk.Label(
    master = frm_tests,
    text='Number of Tests:'
).grid(row = 0,column=1)

tk.Entry(
    master = frm_tests,
    text = "10"
).grid(row = 0,column=2)






def browse_button():
    # Allow user to select a directory and store it in global var
    # called folder_path
    global folder_path
    filename = filedialog.askdirectory()
    folder_path.set(filename)
    updateConsole("Save Location Set")
    print(filename)

button2 = tk.Button(
    master=frm_loc,
    text="Browse", 
    command=browse_button,
    ).grid(sticky='w',row=1, column=0)
lbl1 = tk.Label(
    master=frm_loc,
    textvariable=folder_path
    ).grid(sticky='e',row=1, column=1 )

## </CENTER FRAME CONTENTS>



## <BOT FRAME CONTENTS>
txt_console = tk.Text(
    master = frm_bot,
    width = 40,
    #state = "disabled"
)
txt_console.pack()


## </BOT FRAME CONTENTS>



window.mainloop()



