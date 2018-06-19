# -*- coding: utf-8 -*-

from tkinter import *
from button_methods import ButtonMethods

'''
TODO: 
slider
instructions
machine learning classifying
'''
class App(ButtonMethods):
    
    def __init__(self, master):
        
        topFrame = Frame(master) #container widget
        topFrame.pack() #organizes widgets in blocks
        bottomFrame = Frame(master)
        bottomFrame.pack()
        text_box = Text(topFrame, fg = "green")
        text_box.pack()
        
        self.create_upload_button(topFrame, text_box)
        self.create_save_button(topFrame, text_box)
        self.create_submit_button(bottomFrame, text_box)
        #w = Scale(master, from_=1, to=0, orient=HORIZONTAL)
        #w.pack()
        
    def create_upload_button(self, frame, tb):
        upload = Button(frame, text = "Upload Document", bg = "#66ff66", fg = "black",
                        height = 1, width= 15, relief=RIDGE, font="Helvetica 10",
                        command = lambda: self.upload_text(tb))
        upload.pack(side=LEFT)
        
    def create_save_button(self, frame, tb):
        save = Button(frame, text = "Save", bg = "#66ff66", fg = "black",
                      height = 1, width= 15, relief=RIDGE, font="Helvetica 10",
                      command = lambda: self.save_text(tb))
        save.pack(side=RIGHT)
        
    def create_submit_button(self, frame, tb):
        submit = Button(frame, text = "Submit", bg = "#66ff66", fg = "black",
                        height = 1, width= 15, relief=RIDGE, font="Helvetica 25",
                        command = lambda: self.submit_text(tb))
        submit.pack()

        

        
        
root = Tk()

root.title("Gistify")
root.geometry("400x600")
app = App(root)

root.mainloop()

