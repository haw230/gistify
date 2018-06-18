# -*- coding: utf-8 -*-
"""
Created on Mon Jun  4 17:59:16 2018

@author: Study Mode
"""

from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
import PyPDF2
from prune_text import TextCleaner

class App(TextCleaner):
    
    def __init__(self, master):
        
        topFrame = Frame(master) #container widget
        topFrame.pack() #organizes widgets in blocks
        bottomFrame = Frame(master)
        bottomFrame.pack()
                
        #textbox
        text = Text(topFrame, fg="green")
        text.pack()
        
        #submit button
        '''img = Image.open("C:/Users/Study Mode/Pictures/submit_button.png")
        photo = ImageTk.PhotoImage(img)
        label = Label(image=photo)
        label.image = photo'''
        upload = Button(bottomFrame, text = "Upload Document", bg = "#66ff66", fg = "black",
                        height = 1, width= 15, relief=RIDGE, font="Helvetica 10",
                        command = self.upload_text)
        upload.pack()
        submit = Button(bottomFrame, text = "Submit", bg = "#66ff66", fg = "black",
                        height = 1, width= 15, relief=RIDGE, font="Helvetica 25",
                        command = self.submit_text)
        

        #label.pack()
        submit.pack()
        
        w = Scale(master, from_=1, to=0, orient=HORIZONTAL)
        w.pack()

        
    def submit_text(self):
        
        print(1)
        
    def upload_text(self):
        fileName = filedialog.askopenfilename()
        pdf = PyPDF2.PdfFileReader(fileName)
        extracted_text = ""
        for i in range(pdf.numPages):
            #extractText() returns unicode string
            extracted_text += pdf.getPage(i).extractText()
        extracted_text.encode('utf8')
        TextCleaner.prune_text(self, extracted_text)
        
        
        
root = Tk()

root.title("Gistify")
root.geometry("400x600")
app = App(root)

root.mainloop()

