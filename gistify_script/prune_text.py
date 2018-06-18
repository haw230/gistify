# -*- coding: utf-8 -*-
"""
Created on Sat Jun 16 23:03:35 2018

@author: Study Mode
"""

class TextCleaner:
    def __init__(self):
        pass
    
    def prune_text(self, text):
        text = text.replace('\r', '').replace('\n', '')
        text = ' '.join(text.split())
        print(text)