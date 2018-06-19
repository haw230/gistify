# -*- coding: utf-8 -*-

from tkinter import *
from button_methods import ButtonMethods

class App(ButtonMethods):
    
    def __init__(self, master):
        
        topFrame = Frame(master) #container widget
        topFrame.pack() #organizes widgets in blocks
        bottomFrame = Frame(master)
        bottomFrame.pack()
                
        text_box = Text(topFrame, fg = "green")
        text_box.pack()
        

        upload = Button(bottomFrame, text = "Upload Document", bg = "#66ff66", fg = "black",
                        height = 1, width= 15, relief=RIDGE, font="Helvetica 10",
                        command = lambda: self.upload_text(text_box))
        upload.pack()
        
        save = Button(bottomFrame, text = "Upload Document", bg = "#66ff66", fg = "black",
                      height = 1, width= 15, relief=RIDGE, font="Helvetica 10",
                      command = lambda: self.save_text(text_box))
        
        submit = Button(bottomFrame, text = "Submit", bg = "#66ff66", fg = "black",
                        height = 1, width= 15, relief=RIDGE, font="Helvetica 25",
                        command = lambda: self.submit_text(text_box))
        submit.pack()
        
        w = Scale(master, from_=1, to=0, orient=HORIZONTAL)
        w.pack()

        

        

        
        
root = Tk()

root.title("Gistify")
root.geometry("400x600")
app = App(root)

root.mainloop()

