import os
from tkinter import ttk
import tkinter as tk
import tkinter.font as tkFont
from tkinter import filedialog
import tkinter.messagebox as tkMessage
from PIL import ImageTk, Image

import aes

class Application(ttk.Frame):

    
    def __init__(self, main_window):

        #variables

        v = tk.IntVar(value = 1)
        file_route = tk.StringVar()
        operation_text = tk.StringVar(value="Encrypt")
        key_String = tk.StringVar()
        file_route_text = ""

        #functions

        def get_file_route():
            file_name = filedialog.askopenfilename(initialdir ="C:", title="Open File")
            file_route.set(file_name)

        def check_radios():
            if v.get() == 1:
                operation_text.set("Encrypt")
            elif v.get() == 2:
                operation_text.set("Decrypt")
        
        def operate():
            ok = True

            if len(key_String.get()) != 16:
                tkMessage.showinfo(title=None, message="Key lenght for AES-128 must be 16")
                ok = False
            if len(file_route.get()) == 0:
                tkMessage.showinfo(title=None, message="Select a file")
                ok = False
            if v.get() != 1 and v.get() != 2:
                tkMessage.showinfo(title=None, message="Select an operation")
                ok = False

            if ok:
                status = 1
                if v.get() == 1:
                    status = aes.encrypt_file(key_String.get(), file_route.get(), file_route.get(), 64*1024)
                elif v.get() == 2:
                    status = aes.decrypt_file(key_String.get(), file_route.get(), file_route.get())

                if status == 0:
                    tkMessage.showinfo(title=None, message="The file was processed successfully")
                else:
                    tkMessage.showinfo(title=None, message="ERROR FOUND")
        
        #window config
        super().__init__(main_window)
        main_window.title("AES-128")
        main_window.resizable(False, False)
        main_window.configure(background='#FFFFFF')

         # get screen width and height
        screen_width = main_window.winfo_screenwidth()
        screen_height = main_window.winfo_screenheight()
        width = 730
        height = 220

        # calculate position x and y coordinates
        x = (screen_width/2) - (width/2)
        y = (screen_height/2) - (height/2)
        main_window.geometry('%dx%d+%d+%d' % (width, height, x, y))

        #font style
        fontStyleTitle = tkFont.Font(family="Roboto", size=14)
        fontStyleSub = tkFont.Font(family="Roboto", size=12)
        fontStyleY = tkFont.Font(family="Roboto", size=10)
        xAlignment = 340
    
        ##components

        self.img = ImageTk.PhotoImage(Image.open("C:\\Users\\chistopher\\OneDrive - Instituto Politecnico Nacional\\SeptimoSemestre\\Cryptography\\Tarea0\\bg.png").resize((350, 220), Image.ANTIALIAS))
        imgLabel = tk.Label(
            image = self.img,
            width = 350,
            height = 220,
            borderwidth= 0
        )
        imgLabel.place(x=-30, y=0)

        labelMain = ttk.Label(
            text="AES-128",
            background = '#FFFFFF',
            font=fontStyleTitle
        )
        labelMain.place(x=xAlignment, y=10)

        ##FORM
        labelKey = ttk.Label(
            text = "Key: ",
            background = '#FFFFFF',
            font=fontStyleSub
        )
        labelKey.place(x=xAlignment, y=50)

        keyEntry = tk.Entry(
            width=34,
            font=fontStyleSub,
            background = '#e1ecf4',
            textvariable = key_String,
        )
        keyEntry.place(x=xAlignment+50, y=50)

        fileEntry = tk.Entry(
            width=26,
            font=fontStyleSub,
            background = '#e1ecf4',
            state='disabled',
            textvariable=file_route
        )
        fileEntry.place(x=xAlignment+120, y=84)

        labelOper = ttk.Label(
            text="Select operation: ",
            background = '#FFFFFF',
            font=fontStyleSub
        )
        labelOper.place(x=xAlignment, y=124)

        rad1 = tk.Radiobutton(
            text="Encrypt",
            background = '#FFFFFF',
            padx = 20,
            variable=v,
            value=1,
            font=fontStyleSub,
            command = check_radios
        ).place(x=xAlignment+124, y=124)

        rad2 = tk.Radiobutton(
            text="Decrypt",
            background = '#FFFFFF',
            padx = 20,
            variable=v,
            value=2,
            font=fontStyleSub,
            command = check_radios
        ).place(x=xAlignment+224, y=124)


        ##buttons

        operation = tk.Button(
            textvariable=operation_text,
            width=10,
            foreground="#ffffff", 
            background="#18354c",
            font=fontStyleSub,
            command = operate
        )
        operation.place(x=xAlignment, y=170)

        fileSel = tk.Button(
            text="Select file",
            width=10,
            foreground="#ffffff", 
            background="#18354c",
            font=fontStyleSub,
            command = get_file_route
        )
        fileSel.place(x=xAlignment, y=80)


main_window = tk.Tk()
app = Application(main_window)
app.mainloop()