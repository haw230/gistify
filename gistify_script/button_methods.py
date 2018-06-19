# -*- coding: utf-8 -*-

import PyPDF2 #extracts text from pdf
from tkinter import filedialog #prompts file manager
from tkinter import INSERT
from text_tools import TextTools

class ButtonMethods(TextCleaner):
    def __init__(self):
        pass
    
    def upload_text(self, tb):
        fileName = filedialog.askopenfilename()
        try: #closing file dialog without uploading file creates error
            pdf = PyPDF2.PdfFileReader(fileName)
            extracted_text = ""
            
            for i in range(pdf.numPages):
                #extractText() returns unicode string
                extracted_text += pdf.getPage(i).extractText()
                
            extracted_text.encode('utf8')
            
            tb.insert(INSERT, self.prune_text(extracted_text))
        except (NameError, FileNotFoundError):
            pass
        
    def submit_text(self, tb):
        text = tb.get("1.0","end-1c")
        
        
    def save_text(self):
        pass
        