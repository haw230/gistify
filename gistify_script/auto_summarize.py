# -*- coding: utf-8 -*-
from nltk.corpus import stopwords #filter useless words
from string import punctuation #list of punctuation
from re import sub #get rid of fancy quotes
from nltk.probability import FreqDist #distributes word freq
from heapq import nlargest #sorts words by freq
from collections import defaultdict
from text_tools import TextTools

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