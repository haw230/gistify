# -*- coding: utf-8 -*-

class TextTools:
    def __init__(self):
        pass
    
    def prune_text(self, text):
        text = text.replace('\r', '').replace('\n', '')
        text = ' '.join(text.split())
        return text