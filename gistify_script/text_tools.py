# -*- coding: utf-8 -*-
import re
import docx
import PyPDF2 #extracts text from pdf

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
        if "”" in text: text = text.replace(".”","”.")
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