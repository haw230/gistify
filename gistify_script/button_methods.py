# -*- coding: utf-8 -*-
from tkinter import filedialog, INSERT, messagebox #prompts file manager
from auto_summarize import AutoSummarize

class ButtonMethods(AutoSummarize):
    def __init__(self):
        pass
    
    def upload_text(self, tb):
        fileName = filedialog.askopenfilename(title = "Select a file",
                                              filetypes = (("pdf files","*.pdf"),("text files","*.txt"),("doc files","*.docx")))
        try: #closing file dialog without uploading file creates error
            if(fileName.endswith(".pdf")):
                extracted_text = self.extract_pdf_text(fileName)
            elif(fileName.endswith(".txt")):
                extracted_text = self.extract_txt_text(fileName)
            else:
                extracted_text = self.extract_docx_text(fileName)
            print(extracted_text)
            tb.insert(INSERT, self.prune_text(extracted_text))
        except FileNotFoundError:
            pass 
        
    def save_text(self, tb):
        text = tb.get("1.0","end-1c")
        original = open("Output/original.txt", "w")
        original.write(text)
        original.close()
        
        shortened = open("Output/shortened.txt", "w")
        shortened.write(self.auto_summarize(text))
        shortened.close()
    
    def submit_text(self, tb):
        text = tb.get("1.0","end-1c")
        messagebox.showinfo("Shortened Text", self.auto_summarize(text))
        