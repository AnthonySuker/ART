from tkinter import filedialog
import tkinter as tk
import gen
import json
import os.path


window = tk.Tk()
window.title("ART Shape Image Recognition Tester")

saveFile = False
#string dec
var_save_path = tk.StringVar("")
var_num_tests = tk.StringVar()
var_result = tk.StringVar()

var_shape = tk.StringVar()
var_size = tk.StringVar()
var_colour = tk.StringVar()


#string sets

var_save_path.set("File Save Location")
var_result.set("Results")


#Frames dec
frm_top = tk.Frame(
    master =window,
    pady =10
)
frm_center = tk.Frame(
    master = window,
    pady=10
)
frm_left = tk.Frame(
    master = frm_center,
    pady = 10
)
frm_right = tk.Frame(
    master = frm_center,
    pady=10
)
frm_bottom = tk.Frame(
    master = window,
    pady = 10
)


frm_top.pack()
frm_center.pack()
frm_left.grid(row = 0, column = 0)
frm_right.grid(row = 0, column = 1)
frm_bottom.pack()

#Labels
lbl_title = tk.Label(
    master= frm_top,
    text = 'Welcome to ART Image Tester',
    font = ("Courier",15),
    anchor='w'
)

lbl_status = tk.Label(
    master = frm_right,
    text='OFFLINE',
    fg = 'red'
)

lbl_saveloc = tk.Label(
    master = frm_right,
    textvariable = var_save_path,
    anchor='w'
)

lbl_testresults = tk.Label(
    master = window,
    textvariable = var_result ,
    anchor='w'
)

lbl_error_degree = tk.Label(
    master=frm_left,
    text ='Acceptable error (%)',
    anchor='w'
)

tk.Label(
    master=frm_bottom,
    text = 'Shape Accuracy: '
).grid(row = 0,column=0)

tk.Label(
    master=frm_bottom,
    text='Size Accuracy: '
).grid(row = 1, column =0)

tk.Label(
    master=frm_bottom,
    text='Colour Accuracy: '
).grid(row=2, column=0)

lbl_shape = tk.Label(
    master=frm_bottom,
    textvariable = var_shape
)

lbl_size = tk.Label(
    master=frm_bottom,
    textvariable = var_size
)

lbl_colour = tk.Label(
    master=frm_bottom,
    textvariable = var_colour
)


lbl_shape.grid(row=0, column=1)
lbl_size.grid(row=1, column=1)
lbl_colour.grid(row=2, column=1)

lbl_title.pack()
lbl_status.grid(row = 1, column = 0, padx =15, pady = 3)
lbl_saveloc.grid(row = 2, column = 0, padx =15, pady = 3)
lbl_error_degree.grid(row = 3, column = 0, padx =15, pady = 3)
lbl_testresults.pack()



#functions
def connect():
    if(gen.connect()):
        lbl_status.config(
            text = "ONLINE",
            fg = 'green'
        )
    else:
        var_result.set("Connection failed")

def setSavePath():
    global var_save_path, saveFile
    saveFile = True
    filename = filedialog.askdirectory()
    var_save_path.set(filename)
    print(filename)
    
def startApp():
    global lbl_shape, lbl_size, lbl_colour
    #try:
    var_result.set("starting")
    perc = float(e_error.get())
    num_tests = int(e_num_tests.get())
    #TODO get return to put into console
    output = gen.startUp(num_tests,perc)

    print(perc)

    if(output[0] < (100 -perc)):
        lbl_shape.config(fg = 'red')
    else:
        lbl_shape.config(fg = 'green')

    if(output[1] < (100 -perc)):
        lbl_size.config(fg = 'red')
    else:
        lbl_size.config(fg = 'green')

    if(output[2] < (100 - perc)):
        lbl_colour.config(fg = 'red')
    else:
        lbl_colour.config(fg = 'green')

    var_shape.set(output[0])
    var_size.set(output[1])
    var_colour.set(output[2])

    if(saveFile):
        loc = var_save_path.get()
        name = "output.txt"
        t = os.path.join(loc,name)
        f = open(t,'w')
        s = "Average shape accuracy: %f \nAverage Size accuracy: %f \nAverage Colour Accuracy: %f" % (output[0],output[1],output[2])
        f.write(s)
        f.write("\n\n\n\nGenerated:")
        s = json.dumps(output[4])
        f.write(s)
        f.write('\n\n\n\nresults:')
        s = json.dumps(output[4])
        f.write(s)

    #except:
        #var_result.set("Make sure both entry values are numbers")



#buttons
btn_connect = tk.Button(
    master=frm_left,
    text = 'Connect',
    command = connect,
    anchor='w'
)

btn_saveloc = tk.Button(
    master=frm_left,
    text = 'log location',
    command = setSavePath,
    anchor='w'
)

btn_start = tk.Button(
    master=frm_left,
    text = 'Start',
    command = startApp,
    anchor='w'
)

btn_connect.grid(row = 1, column = 0, padx=15, pady = 3)
btn_saveloc.grid(row = 2, column = 0, padx=15, pady = 3)
btn_start.grid(row = 4, column = 0, padx=15, pady = 3)


#entry fields

e_error = tk.Entry(
    master=frm_right
)

e_num_tests = tk.Entry(
    master=frm_right,
)

e_num_tests.insert(tk.END,'Number of tests')
e_error.grid(row = 3, column = 0, padx=30, pady = 3)
e_num_tests.grid(row = 4, column = 0, padx=15, pady = 3)





window.mainloop()