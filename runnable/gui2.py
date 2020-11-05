from tkinter import filedialog
import tkinter as tk
import gen


window = tk.Tk()
window.title("ART Shape Image Recognition Tester")

#string dec
var_save_path = tk.StringVar()
var_num_tests = tk.StringVar()
var_result = tk.StringVar()


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


frm_top.pack()
frm_center.pack()
frm_left.grid(row = 0, column = 0)
frm_right.grid(row = 0, column = 1)


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
    global var_save_path
    filename = filedialog.askdirectory()
    var_save_path.set(filename)
    updateConsole("Save Location Set")
    print(filename)
    
def startApp():
    try:
        perc = float(e_error.get())
        num_tests = int(e_num_tests.get())
        print(num_tests)
        print(perc)
    except:
        var_result.set("Make sure both entry values are numbers")
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

lbl_title.pack()
lbl_status.grid(row = 1, column = 0, padx =15, pady = 3)
lbl_saveloc.grid(row = 2, column = 0, padx =15, pady = 3)
lbl_error_degree.grid(row = 3, column = 0, padx =15, pady = 3)
lbl_testresults.pack()


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