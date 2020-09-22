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



def start_button():
    global started, btn_start, lbl_status_actual
    started = not started
    if started:
        startBtnVar.set('Stop')
        lbl_status_actual.config(
            text = "ONLINE",
            fg = 'green'
        )
        updateConsole("Started")
    else:
        startBtnVar.set('Start')
        lbl_status_actual.config(
            text = "OFFLINE",
            fg = 'red'
        )
        updateConsole("Stopped")

    

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


#g = tk.Label(text='Hello')
#g.pack()

window.mainloop()