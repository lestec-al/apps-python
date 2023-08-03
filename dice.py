import time, random

def dice_pysimplegui():
    import PySimpleGUI as sg
    # Window settings
    sg.theme("DefaultNoMoreNagging")
    count = 0
    layout = [
        [
            sg.Text("Roll dice between", font=("Helvetica", 15), size=(15,1)),
            sg.Input(default_text=1, background_color="lightgrey", size=(2,1), key="-INPUT1-", font=("Helvetica", 16)),
            sg.Text("&", font=("Helvetica", 15), size=(2,1)),
            sg.Input(default_text=6, background_color="lightgrey", size=(2,1), key="-INPUT2-", font=("Helvetica", 16))
        ],
        [sg.Text(key="-OUTPUT-", text_color="green", justification="center", font=("Helvetica", 30), size=(20,1))],
        [
            sg.Button("CLEAN", button_color="red"),
            sg.Text(str(count) + "/10", key="-OUTPUT1-", font=("Helvetica", 12), size=(10,1)),
            sg.Input(key="-OUTPUT2-", font=("Helvetica", 12), readonly=True, size=(20,1))
        ],
        [sg.Button("START", button_color="green", size=(6,2), font=("Helvetica", 12, "bold"))] ]
    window = sg.Window("Dice", layout, element_justification="center", return_keyboard_events=True, debugger_enabled=False, finalize=True, text_justification="center", icon='data/dice.png')
    # Main loop
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        my_string1 = values["-INPUT1-"]
        my_string2 = values["-INPUT2-"]
        values1 = values["-OUTPUT2-"]
        # Input validation
        if count >= 10:
            event = "CLEAN"
        if len(my_string1) >= 2 or "0" in my_string1:
            window["-INPUT1-"].update(my_string1[:-1])
        if len(my_string2) >= 2 or "0" in my_string2:
            window["-INPUT2-"].update(my_string2[:-1])
        # Buttons events
        if event == "START":
            try:
                my_string1 = int(my_string1)
                my_string2 = int(my_string2)
            except:
                window["-OUTPUT-"].update("Write a numbers")
                continue
            time.sleep(0.5)
            numx = random.randint(int(my_string1), int(my_string2))
            window["-OUTPUT-"].update(str(numx))
            count += 1
            values1 = values1 + " " + str(numx)
            window["-OUTPUT1-"].update(str(count) + "/10")
            window["-OUTPUT2-"].update(values1)
        if event == "CLEAN":
            numx = ""
            count = 0
            values1 = ""
            window["-OUTPUT-"].update(numx)
            window["-OUTPUT1-"].update(str(count) + "/10")
            window["-OUTPUT2-"].update(values1)

def dice_tkinter():
    import tkinter as tk
    import sys, platform
    # Fix graphic on Win 10
    if sys.platform == "win32" and platform.release() == "10":
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    # Operations
    def start():
        my_string1 = entry1.get()
        my_string2 = entry2.get()
        if count[0] >= 10:
            clean()
        elif len(my_string1) >= 2 or len(my_string2) >= 2:
            label["text"]="Too many symbols"
        else:
            try:
                time.sleep(0.5)
                numx = random.randint(int(my_string1), int(my_string2))
                label["text"]=str(numx)
                count[0] += 1
                label2["text"]=str(count[0]) + "/10:"
                label3["text"]=label3["text"] + " " + str(numx)
            except ValueError:
                label["text"]="Write a numbers"
    def clean():
        count[0] = 0
        label["text"]=""
        label2["text"]="0/10:"
        label3["text"]=""
    # Window settings
    count = [0]
    window = tk.Tk()
    window.resizable(False, False)
    window.title("Dice")
    window.iconphoto(False, tk.PhotoImage(file='data/dice.png'))
    frame = tk.Frame(window, border=8)
    frame.pack()
    frame1 = tk.Frame(frame)
    frame1.pack()
    tk.Label(frame1, text="Roll dice between", font="size= 14", anchor="w").grid(column=0, row=0, columnspan=2)
    entry1 = tk.Entry(frame1, width=3, background="lightgrey", font="size= 16", justify="center", highlightcolor="white", highlightthickness=0)
    entry1.grid(column=2, row=0)
    entry1.insert("end", "1")
    tk.Label(frame1, text="and", font="size= 14", anchor="w").grid(column=3, row=0)
    entry2 = tk.Entry(frame1, width=3, background="lightgrey", font="size= 16", justify="center", highlightcolor="white", highlightthickness=0)
    entry2.grid(column=4, row=0)
    entry2.insert("end", "6")
    label = tk.Label(frame, fg="green", font="size= 26", anchor="w")
    label.pack()
    tk.Button(frame, bg="green", fg="white",  text="START", height=1, width=6, font=("Helvetica", 16), command=start).pack(side='bottom')
    frame2 = tk.Frame(frame, border=5)
    frame2.pack(side="left")
    tk.Button(frame2, text="✖", fg="white", bg="red", height=1, width=3, font=("Helvetica", 12), command=clean).grid(column=0, row=0)
    label2 = tk.Label(frame2, text="0/10:", font="size= 14", anchor="w")
    label2.grid(column=1, row=0)
    label3 = tk.Label(frame2, font="size= 14", anchor="w")
    label3.grid(column=2, row=0, columnspan=3)
    window.mainloop()

if __name__ == "__main__":
    # Game options: dice_tkinter(), dice_pysimplegui()
    dice_tkinter()