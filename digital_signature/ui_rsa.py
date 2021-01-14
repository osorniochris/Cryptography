import os
from tkinter import ttk
import tkinter as tk
import tkinter.font as tkFont
from tkinter import filedialog
import tkinter.messagebox as tkMessage

import digital_sign_reciever as verifier
import digital_sign_sender as signer

class DigitalSignature(ttk.Frame):
    def __init__(self, main_window):

        #variables
        v = tk.IntVar(value = 1)
        file_route = tk.StringVar()
        key_route = tk.StringVar()
        operation_text = tk.StringVar(value="Sign")

        #functions
        def get_file_route():
            file_name = filedialog.askopenfilename(initialdir ="C:", title="Open File")
            file_route.set(file_name)

        def get_key_route():
            file_name = filedialog.askopenfilename(initialdir ="C:", title="Open File")
            key_route.set(file_name)

        def check_radios():
            if v.get() == 1:
                operation_text.set("Sign")
            elif v.get() == 2:
                operation_text.set("Verify")
        
        def operate():
            ok = True

            if len(file_route.get()) == 0:
                tkMessage.showinfo(title=None, message="Select a file")
                ok = False
            if len(key_route.get()) == 0:
                tkMessage.showinfo(title=None, message="Select a key file")
                ok = False
            if v.get() != 1 and v.get() != 2:
                tkMessage.showinfo(title=None, message="Select an operation")
                ok = False

            if ok:
                message = ""
                if v.get() == 1:
                    message = signer.sign_file(file_route.get(), key_route.get())
                else:
                    message = verifier.check_signature(file_route.get(), key_route.get())
                
                tkMessage.showinfo(title=None, message=message)
        
        #window config
        super().__init__(main_window)
        main_window.title("Digital Signature")
        main_window.resizable(False, False)
        main_window.configure(background='#FFFFFF')

         # get screen width and height
        screen_width = main_window.winfo_screenwidth()
        screen_height = main_window.winfo_screenheight()
        width = 420
        height = 340

        # calculate position x and y coordinates
        x = (screen_width/2) - (width/2)
        y = (screen_height/2) - (height/2)
        main_window.geometry('%dx%d+%d+%d' % (width, height, x, y))

        #font style
        fontStyleTitle = tkFont.Font(family="Roboto", size=14)
        fontStyleSub = tkFont.Font(family="Roboto", size=12)
        xAlignment = 30
    
        ##components
        labelMain = ttk.Label(
            text="Digital Signature",
            background = '#FFFFFF',
            font=fontStyleTitle
        )
        labelMain.place(x=xAlignment, y=10)

        ##FORM

        fileEntry = tk.Entry(
            width=26,
            font=fontStyleSub,
            background = '#e1ecf4',
            state='disabled',
            textvariable=file_route
        )
        fileEntry.place(x=xAlignment+120, y=154)

        keyEntry = tk.Entry(
            width=26,
            font=fontStyleSub,
            background = '#e1ecf4',
            state='disabled',
            textvariable=key_route
        )
        keyEntry.place(x=xAlignment+120, y=204)

        labelOper = ttk.Label(
            text="Select operation: ",
            background = '#FFFFFF',
            font=fontStyleSub
        )
        labelOper.place(x=xAlignment, y=50)

        rad1 = tk.Radiobutton(
            text="Sign file",
            background = '#FFFFFF',
            padx = 20,
            variable=v,
            value=1,
            font=fontStyleSub,
            command = check_radios
        ).place(x=xAlignment+124, y=50)

        rad2 = tk.Radiobutton(
            text="Verify signature",
            background = '#FFFFFF',
            padx = 20,
            variable=v,
            value=2,
            font=fontStyleSub,
            command = check_radios
        ).place(x=xAlignment+124, y=76)


        ##buttons
        operation = tk.Button(
            textvariable=operation_text,
            width=10,
            foreground="#ffffff", 
            background="#2e0049",
            font=fontStyleSub,
            command = operate
        )
        operation.place(x=xAlignment, y=270)

        fileSel = tk.Button(
            text="Select file",
            width=10,
            foreground="#ffffff", 
            background="#2e0049",
            font=fontStyleSub,
            command = get_file_route
        )
        fileSel.place(x=xAlignment, y=150)

        keySel = tk.Button(
            text="Select key",
            width=10,
            foreground="#ffffff", 
            background="#2e0049",
            font=fontStyleSub,
            command = get_key_route
        )
        keySel.place(x=xAlignment, y=200)

        


main_window = tk.Tk()
app = DigitalSignature(main_window)
app.mainloop()