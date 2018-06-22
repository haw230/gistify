
import sys
sys.path.insert(0, "C:/ProgramData/Anaconda3/lib/site-packages")
sys.setrecursionlimit(100000)

from tkinter import filedialog, INSERT, messagebox #prompts file manager
from nltk.corpus import stopwords #filter useless words
from string import punctuation #list of punctuation
from re import sub #get rid of fancy quotes
from nltk.probability import FreqDist #distributes word freq
from heapq import nlargest #sorts words by freq
from collections import defaultdict
import re
import docx
import PyPDF2 #extracts text from pdf
from tkinter import *
import py2exe


caps = "([A-Z])"
prefixes = "(Mr|St|Mrs|Ms|Dr)[.]"
suffixes = "(Inc|Ltd|Jr|Sr|Co)"
starters = "(Mr|Mrs|Ms|Dr|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)"
acronyms = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
websites = "[.](com|net|org|io|gov)"

class TextTools:
    def __init__(self):
        pass
    
    def prune_text(self, text):
        text = text.replace('\r', '').replace('\n', '')
        text = ' '.join(text.split())
        return text
    
    def text_is_valid(self, text):
        if(len(tokeniz_sent(text)) > 1):
            return True
        return False
    
    def tokenize_sent(self, text):
        text = " " + text + "  "
        text = text.replace("\n"," ")
        text = re.sub(prefixes,"\\1<prd>",text)
        text = re.sub(websites,"<prd>\\1",text)
        if "Ph.D" in text: text = text.replace("Ph.D.","Ph<prd>D<prd>")
        text = re.sub("\s" + caps + "[.] "," \\1<prd> ",text)
        text = re.sub(acronyms+" "+starters,"\\1<stop> \\2",text)
        text = re.sub(caps + "[.]" + caps + "[.]" + caps + "[.]","\\1<prd>\\2<prd>\\3<prd>",text)
        text = re.sub(caps + "[.]" + caps + "[.]","\\1<prd>\\2<prd>",text)
        text = re.sub(" "+suffixes+"[.] "+starters," \\1<stop> \\2",text)
        text = re.sub(" "+suffixes+"[.]"," \\1<prd>",text)
        text = re.sub(" " + caps + "[.]"," \\1<prd>",text)
        if "\"" in text: text = text.replace(".\"","\".")
        if "!" in text: text = text.replace("!\"","\"!")
        if "?" in text: text = text.replace("?\"","\"?")
        text = text.replace(".",".<stop>")
        text = text.replace("?","?<stop>")
        text = text.replace("!","!<stop>")
        text = text.replace("<prd>",".")
        sentences = text.split("<stop>")
        sentences = sentences[:-1]
        sentences = [s.strip() for s in sentences]
        return sentences
    
    def tokenize_words(self, text):
        return text.split()
    
    def extract_pdf_text(self, file):
        pdf = PyPDF2.PdfFileReader(file)
        extracted_text = ""
        if(pdf.isEncrypted):
            pdf.decrypt("")
        for i in range(pdf.numPages):
            #extractText() returns unicode string
            extracted_text += pdf.getPage(i).extractText()
            
        extracted_text.encode('utf8')
        return extracted_text
        
    def extract_txt_text(self, file):
        text = open(file, "r")
        #print(text.read())
        return text.read()
    
    def extract_docx_text(self, file):
        doc = docx.Document(file)
        fullText = []
        for para in doc.paragraphs:
            fullText.append(para.text)
        return "\n".join(fullText)

class AutoSummarize(TextTools):
    def auto_summarize(self, text):
        #u = unicode string, \xa0 = space
        text = sub(u'[\u201c\u201d\u2019]',"'",text.replace(u'\xa0', u' '))
        
        #preprocessing
        sents = self.tokenize_sent(text)
        sent = self.tokenize_sent(text) #have to maintain original copy
        words = self.tokenize_words(text.lower())
        
        #list of common words and punctuation to be removed
        stop_words = set(stopwords.words('english') + list(punctuation))
        
        words = [word for word in words if word not in stop_words and not self.is_number(word)]
        
        freq = FreqDist(words)
        nlargest(10, freq, key = freq.get) #top 10, in "freq" distribution, ranked by value
        
        #defaultdict creates any key that is called but does not exist
        #calls "int()" for default items
        ranking = defaultdict(int)
        for i, sents in enumerate(sents): #enumerate converts [a,b,c] to [(0,a),(1,b),(2,c)]
            for w in self.tokenize_words(sents.lower()):
                if w in freq:
                    ranking[i] += freq[w] #adding importance
                    
        #four most important sentences
        sents_idx = nlargest(4, ranking, key=ranking.get)
                    
        top_sentences = " ".join([sent[j] for j in sorted(sents_idx)])
        return top_sentences

    def is_number(self, x):
        try:
            int(x)
            return True
        except ValueError:
            return False

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
