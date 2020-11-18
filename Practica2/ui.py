import os
from tkinter import ttk
import tkinter as tk
import tkinter.font as tkFont
from tkinter import filedialog
import tkinter.messagebox as tkMessage

import DES

class Menu(ttk.Frame):
    def __init__(self, main_window):

        #variables
        v = tk.IntVar(value = 1)
        v_1 = tk.IntVar(value = 0)
        v_2 = tk.IntVar(value = 0)
        v_3 = tk.IntVar(value = 0)
        v_4 = tk.IntVar(value = 0)
        file_route = tk.StringVar()
        operation_text = tk.StringVar(value="Encrypt")
        key_String = tk.StringVar()

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
            
            if len(key_String.get()) == 0:
                tkMessage.showinfo(title=None, message="Insert a key")
                ok = False
            if len(file_route.get()) == 0:
                tkMessage.showinfo(title=None, message="Select a file")
                ok = False
            if v.get() != 1 and v.get() != 2:
                tkMessage.showinfo(title=None, message="Select an operation")
                ok = False
            if len(key_String.get()) != 8 :
                tkMessage.showinfo(title=None, message="Invalid Key. Must be 8 characters long")
                ok = False
            if v_1.get() == 0 and v_2.get() == 0 and v_3.get() == 0 and v_4.get() == 0:
                tkMessage.showinfo(title=None, message="Select a Mode of Operation")
                ok = False

            if ok:
                if v.get() == 1:
                    if v_1.get() == 1:
                        DES.des(bytes(key_String.get(), 'utf-8'), file_route.get(), DES.ENCRYPT, DES.ECB)
                    if v_2.get() == 1:
                        DES.des(bytes(key_String.get(), 'utf-8'), file_route.get(), DES.ENCRYPT, DES.CBC)
                    if v_3.get() == 1:
                        DES.des(bytes(key_String.get(), 'utf-8'), file_route.get(), DES.ENCRYPT, DES.CFB)
                    if v_4.get() == 1:
                        DES.des(bytes(key_String.get(), 'utf-8'), file_route.get(), DES.ENCRYPT, DES.OFB)
                if v.get() == 2:
                    if v_1.get() == 1:
                        DES.des(bytes(key_String.get(), 'utf-8'), file_route.get(), DES.DECRYPT, DES.ECB)
                    if v_2.get() == 1:
                        DES.des(bytes(key_String.get(), 'utf-8'), file_route.get(), DES.DECRYPT, DES.CBC)
                    if v_3.get() == 1:
                        DES.des(bytes(key_String.get(), 'utf-8'), file_route.get(), DES.DECRYPT, DES.CFB)
                    if v_4.get() == 1:
                        DES.des(bytes(key_String.get(), 'utf-8'), file_route.get(), DES.DECRYPT, DES.OFB)
                
                tkMessage.showinfo(title=None, message="Process completed!")
        
        #window config
        super().__init__(main_window)
        main_window.title("DES")
        main_window.resizable(False, False)
        main_window.configure(background='#FFFFFF')

         # get screen width and height
        screen_width = main_window.winfo_screenwidth()
        screen_height = main_window.winfo_screenheight()
        width = 420
        height = 450

        # calculate position x and y coordinates
        x = (screen_width/2) - (width/2)
        y = (screen_height/2) - (height/2)
        main_window.geometry('%dx%d+%d+%d' % (width, height, x, y))

        #font style
        fontStyleTitle = tkFont.Font(family="Roboto", size=20)
        fontStyleSub = tkFont.Font(family="Roboto", size=12)
        xAlignment = 30
    
        ##components
        labelMain = ttk.Label(
            text="DES",
            background = '#FFFFFF',
            font=fontStyleTitle
        )
        labelMain.place(x=xAlignment+140, y=10)

        ##FORM
        labelKey = ttk.Label(
            text = "Key: ",
            background = '#FFFFFF',
            font=fontStyleSub
        )
        labelKey.place(x=xAlignment, y=150)

        keyEntry = tk.Entry(
            width=34,
            font=fontStyleSub,
            background="#00863d",
            foreground="#ffffff", 
            textvariable = key_String,
        )
        keyEntry.place(x=xAlignment+50, y=150)

        fileEntry = tk.Entry(
            width=26,
            font=fontStyleSub,
            background="#00863d",
            state='disabled',
            textvariable=file_route
        )
        fileEntry.place(x=xAlignment+120, y=64)

        labelOper = ttk.Label(
            text="Select operation: ",
            background = '#FFFFFF',
            font=fontStyleSub
        )
        labelOper.place(x=xAlignment, y=104)

        labelMode = ttk.Label(
            text="Modes of operation:",
            background = '#FFFFFF',
            font=fontStyleSub
        )
        labelMode.place(x=xAlignment, y=208)

        rad1 = tk.Radiobutton(
            text="Encrypt",
            background = '#FFFFFF',
            padx = 20,
            variable=v,
            value=1,
            font=fontStyleSub,
            command = check_radios
        ).place(x=xAlignment+124, y=104)

        rad2 = tk.Radiobutton(
            text="Decrypt",
            background = '#FFFFFF',
            padx = 20,
            variable=v,
            value=2,
            font=fontStyleSub,
            command = check_radios
        ).place(x=xAlignment+224, y=104)

        #check buttons
        ecb= tk.Checkbutton(
            text='Electronic Codebook (ECB)',
            background = '#FFFFFF',
            font=fontStyleSub,
            variable=v_1, 
            onvalue=1, 
            offvalue=0
        ).place(x= xAlignment, y = 244)

        cbc= tk.Checkbutton(
            text='Cipher Block Chaining (CBC)',
            background = '#FFFFFF',
            font=fontStyleSub,
            variable=v_2, 
            onvalue=1, 
            offvalue=0
        ).place(x= xAlignment, y = 270)

        cfb= tk.Checkbutton(
            text='Cipher Feedback (CFB)',
            background = '#FFFFFF',
            font=fontStyleSub,
            variable=v_3, 
            onvalue=1, 
            offvalue=0
        ).place(x= xAlignment, y = 296)

        ofb= tk.Checkbutton(
            text='Output Feedback (OFB)',
            background = '#FFFFFF',
            font=fontStyleSub,
            variable=v_4, 
            onvalue=1, 
            offvalue=0
        ).place(x= xAlignment, y = 322)

        ##buttons
        operation = tk.Button(
            textvariable=operation_text,
            width=10,
            foreground="#ffffff", 
            background="#00863d",
            font=fontStyleSub,
            command = operate
        )
        operation.place(x=xAlignment, y=380)

        fileSel = tk.Button(
            text="Select file",
            width=10,
            foreground="#ffffff", 
            background="#00863d",
            font=fontStyleSub,
            command = get_file_route
        )
        fileSel.place(x=xAlignment, y=60)


main_window = tk.Tk()
app = Menu(main_window)
app.mainloop()