from tkinter import ttk
import tkinter as tk
import tkinter.font as tkFont
from tkinter import filedialog
from tkinter import simpledialog
import tkinter.messagebox as tkMessage

import generate_key_pair
import digital_sign_reciever as verifier
import digital_sign_sender as signer
import aes_rsa


class Menu(ttk.Frame):

    def __init__(self, main_window):

        #variables
        v = tk.IntVar(value = 1)
        go_text = tk.StringVar(value="Ok")

        #functions
        def check_radios():
            if v.get() == 1:
                main_window.destroy()
            
                other_window = tk.Tk()
                app = Encryption(other_window)
                app.mainloop()
            elif v.get() == 2:
                main_window.destroy()
            
                other_window = tk.Tk()
                app = DigitalSignature(other_window)
                app.mainloop()
            elif v.get() == 3:
                main_window.destroy()
            
                other_window = tk.Tk()
                app = AllServices(other_window)
                app.mainloop()
            elif v.get() == 4:
                name = simpledialog.askstring('Key generation', 'Introduce a name for your key file')
                if name != None:
                    if len(name) != 0:
                        size = simpledialog.askstring('Key generation', 'Introduce a key size (1024, 2048 or 3072)')
                        if size != None:
                            if (len(size) != 0 )and (size in {"1024", "2048", "3072"}):
                                result = generate_key_pair.create_key(name, size)
                                tkMessage.showinfo(title=None, message=result)
                            else:
                                tkMessage.showinfo(title=None, message="Invalid key size")
            
        #window config
        super().__init__(main_window)
        main_window.title("Select an option")
        main_window.resizable(False, False)
        main_window.configure(background='#FFFFFF')

         # get screen width and height
        screen_width = main_window.winfo_screenwidth()
        screen_height = main_window.winfo_screenheight()
        width = 400
        height = 250

        # calculate position x and y coordinates
        x = (screen_width/2) - (width/2)
        y = (screen_height/2) - (height/2)
        main_window.geometry('%dx%d+%d+%d' % (width, height, x, y))

        #font style
        fontStyleSub = tkFont.Font(family="Roboto", size=12)
        xAlignment = 30
    
        ##components

        self.labelOper = ttk.Label(
            text="Select an option: ",
            background = '#FFFFFF',
            font=fontStyleSub
        ).place(x=xAlignment, y=20)

        rad1 = tk.Radiobutton(
            text="Encryption / Decryption",
            background = '#FFFFFF',
            padx = 20,
            variable=v,
            value=1,
            font=fontStyleSub
        ).place(x=xAlignment, y=60)

        rad2 = tk.Radiobutton(
            text="Signature / Verification",
            background = '#FFFFFF',
            padx = 20,
            variable=v,
            value=2,
            font=fontStyleSub
        ).place(x=xAlignment, y=90)

        rad3 = tk.Radiobutton(
            text="All services",
            background = '#FFFFFF',
            padx = 20,
            variable=v,
            value=3,
            font=fontStyleSub
        ).place(x=xAlignment, y=120)

        rad4 = tk.Radiobutton(
            text="Generate RSA Key",
            background = '#FFFFFF',
            padx = 20,
            variable=v,
            value=4,
            font=fontStyleSub
        ).place(x=xAlignment, y=150)

        ##button
        self.go = tk.Button(
            textvariable=go_text,
            width=10,
            foreground="#ffffff", 
            background="#f2629d",
            font=fontStyleSub,
            command = check_radios
        ).place(x=xAlignment, y=200)

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

        def back():
            main_window.destroy()
            
            other_window = tk.Tk()
            app = Menu(other_window)
            app.mainloop()
        
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
            background="#f2629d",
            font=fontStyleSub,
            command = operate
        )
        operation.place(x=xAlignment, y=270)

        back = tk.Button(
            text="Go back",
            width=10,
            foreground="#ffffff", 
            background="#f2629d",
            font=fontStyleSub,
            command = back
        )
        back.place(x=xAlignment+258, y=270)

        fileSel = tk.Button(
            text="Select file",
            width=10,
            foreground="#ffffff", 
            background="#f2629d",
            font=fontStyleSub,
            command = get_file_route
        )
        fileSel.place(x=xAlignment, y=150)

        keySel = tk.Button(
            text="Select key",
            width=10,
            foreground="#ffffff", 
            background="#f2629d",
            font=fontStyleSub,
            command = get_key_route
        )
        keySel.place(x=xAlignment, y=200)

class Encryption(ttk.Frame):
    def __init__(self, main_window):

        #variables
        v = tk.IntVar(value = 1)
        file_route = tk.StringVar()
        key_route = tk.StringVar()
        operation_text = tk.StringVar(value="Encrypt")

        #functions
        def get_file_route():
            file_name = filedialog.askopenfilename(initialdir ="C:", title="Open File")
            file_route.set(file_name)

        def get_key_route():
            file_name = filedialog.askopenfilename(initialdir ="C:", title="Open File")
            key_route.set(file_name)

        def check_radios():
            if v.get() == 1:
                operation_text.set("Encrypt")
            elif v.get() == 2:
                operation_text.set("Decrypt")

        def back():
            main_window.destroy()
            
            other_window = tk.Tk()
            app = Menu(other_window)
            app.mainloop()
        
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
                    message = aes_rsa.encrypt(file_route.get(), key_route.get())
                else:
                    message = aes_rsa.decrypt(file_route.get(), key_route.get())
                
                tkMessage.showinfo(title=None, message=message)
        
        #window config
        super().__init__(main_window)
        main_window.title("AES Encryption")
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
            text="AES Encryption",
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
            text="Encrypt",
            background = '#FFFFFF',
            padx = 20,
            variable=v,
            value=1,
            font=fontStyleSub,
            command = check_radios
        ).place(x=xAlignment+124, y=50)

        rad2 = tk.Radiobutton(
            text="Decrypt",
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
            background="#f2629d",
            font=fontStyleSub,
            command = operate
        )
        operation.place(x=xAlignment, y=270)

        back = tk.Button(
            text="Go back",
            width=10,
            foreground="#ffffff", 
            background="#f2629d",
            font=fontStyleSub,
            command = back
        )
        back.place(x=xAlignment+258, y=270)

        fileSel = tk.Button(
            text="Select file",
            width=10,
            foreground="#ffffff", 
            background="#f2629d",
            font=fontStyleSub,
            command = get_file_route
        )
        fileSel.place(x=xAlignment, y=150)

        keySel = tk.Button(
            text="RSA key",
            width=10,
            foreground="#ffffff", 
            background="#f2629d",
            font=fontStyleSub,
            command = get_key_route
        )
        keySel.place(x=xAlignment, y=200)

class AllServices(ttk.Frame):
    def __init__(self, main_window):

        #variables
        v = tk.IntVar(value = 1)
        file_route = tk.StringVar()
        public_key_route = tk.StringVar()
        private_key_route = tk.StringVar()
        operation_text = tk.StringVar(value="Generate file")

        #functions
        def get_file_route():
            file_name = filedialog.askopenfilename(initialdir ="C:", title="Open File")
            file_route.set(file_name)

        def get_public_key_route():
            file_name = filedialog.askopenfilename(initialdir ="C:", title="Open File")
            public_key_route.set(file_name)
        
        def get_private_key_route():
            file_name = filedialog.askopenfilename(initialdir ="C:", title="Open File")
            private_key_route.set(file_name)

        def check_radios():
            if v.get() == 1:
                operation_text.set("Generate file")
            elif v.get() == 2:
                operation_text.set("Check file")

        def back():
            main_window.destroy()
            
            other_window = tk.Tk()
            app = Menu(other_window)
            app.mainloop()
        
        def operate():
            ok = True

            if len(file_route.get()) == 0:
                tkMessage.showinfo(title=None, message="Select a file")
                ok = False
            if len(public_key_route.get()) == 0:
                tkMessage.showinfo(title=None, message="Select a public key file")
                ok = False
            if len(private_key_route.get()) == 0:
                tkMessage.showinfo(title=None, message="Select a private key file")
                ok = False
            if v.get() != 1 and v.get() != 2:
                tkMessage.showinfo(title=None, message="Select an operation")
                ok = False

            if ok:
                message = ""
                if v.get() == 1:
                    message = aes_rsa.encrypt_and_sign(file_route.get(), public_key_route.get(), private_key_route.get())
                else:
                    message = aes_rsa.decrypt_and_verify(file_route.get(), public_key_route.get(), private_key_route.get())
                
                tkMessage.showinfo(title=None, message=message)
        
        #window config
        super().__init__(main_window)
        main_window.title("Hybrid Cryptography")
        main_window.resizable(False, False)
        main_window.configure(background='#FFFFFF')

         # get screen width and height
        screen_width = main_window.winfo_screenwidth()
        screen_height = main_window.winfo_screenheight()
        width = 420
        height = 420

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
            text="Hybrid Cryptography",
            background = '#FFFFFF',
            font=fontStyleTitle
        )
        labelMain.place(x=xAlignment, y=10)

        ##FORM

        fileEntry = tk.Entry(
            width=25,
            font=fontStyleSub,
            background = '#e1ecf4',
            state='disabled',
            textvariable=file_route
        )
        fileEntry.place(x=xAlignment+130, y=154)

        publickeyEntry = tk.Entry(
            width=25,
            font=fontStyleSub,
            background = '#e1ecf4',
            state='disabled',
            textvariable=public_key_route
        )
        publickeyEntry.place(x=xAlignment+130, y=204)

        privatekeyEntry = tk.Entry(
            width=25,
            font=fontStyleSub,
            background = '#e1ecf4',
            state='disabled',
            textvariable=private_key_route
        )
        privatekeyEntry.place(x=xAlignment+130, y=254)

        labelOper = ttk.Label(
            text="Select operation: ",
            background = '#FFFFFF',
            font=fontStyleSub
        )
        labelOper.place(x=xAlignment, y=50)

        rad1 = tk.Radiobutton(
            text="Encrypt and Sign",
            background = '#FFFFFF',
            padx = 20,
            variable=v,
            value=1,
            font=fontStyleSub,
            command = check_radios
        ).place(x=xAlignment+124, y=50)

        rad2 = tk.Radiobutton(
            text="Decrypt and Verify",
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
            width=14,
            foreground="#ffffff", 
            background="#f2629d",
            font=fontStyleSub,
            command = operate
        )
        operation.place(x=xAlignment, y=340)

        back = tk.Button(
            text="Go back",
            width=10,
            foreground="#ffffff", 
            background="#f2629d",
            font=fontStyleSub,
            command = back
        )
        back.place(x=xAlignment+258, y=340)

        fileSel = tk.Button(
            text="Select file",
            width=12,
            foreground="#ffffff", 
            background="#f2629d",
            font=fontStyleSub,
            command = get_file_route
        )
        fileSel.place(x=xAlignment, y=150)

        publickeySel = tk.Button(
            text="Public RSA key",
            width=12,
            foreground="#ffffff", 
            background="#f2629d",
            font=fontStyleSub,
            command = get_public_key_route
        )
        publickeySel.place(x=xAlignment, y=200)

        privatekeySel = tk.Button(
            text="Private RSA key",
            width=12,
            foreground="#ffffff", 
            background="#f2629d",
            font=fontStyleSub,
            command = get_private_key_route
        )
        privatekeySel.place(x=xAlignment, y=250)

main_window = tk.Tk()
app = Menu(main_window)
app.mainloop()