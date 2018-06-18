# -*- coding: utf-8 -*-
"""
Created on Sat Jun  2 22:01:13 2018

@author: Study Mode
"""

import requests #downloads webpage
from lxml import html #formats webpage
from nltk.tokenize import sent_tokenize, word_tokenize #break text up
from nltk.corpus import stopwords #filter useless words
from string import punctuation #list of punctuation
from re import sub #get rid of fancy quotes
from nltk.probability import FreqDist #distributes word freq
from heapq import nlargest #sorts words by freq
from collections import defaultdict

def is_number(x):
    try:
        int(x)
        return True
    except ValueError:
        return False

#extract article
url = "https://uwaterloo.ca/stories/waterloo-ranked-1-school-canada-computer-science-engineering"
page = requests.get(url)
tree = html.fromstring(page.content)
tree.xpath('//p/text()')
text = ' '.join(tree.xpath('//p/text()'))

#u = unicode string, \xa0 = space
text = sub(u'[\u201c\u201d\u2019]',"'",text.replace(u'\xa0', u' '))

#preprocessing
sents = sent_tokenize(text)
sent = sent_tokenize(text)
words = word_tokenize(text.lower())

#list of common words and punctuation to be removed
stop_words = set(stopwords.words('english') + list(punctuation))

words = [word for word in words if word not in stop_words and not is_number(word)]

freq = FreqDist(words)
nlargest(10, freq, key = freq.get) #top 10, in "freq" distribution, ranked by value

#defaultdict creates any key that is called but does not exist
#calls "int()" for default items
ranking = defaultdict(int)
for i, sents in enumerate(sents): #enumerate converts [a,b,c] to [(0,a),(1,b),(2,c)]
    for w in word_tokenize(sents.lower()):
        if w in freq:
            ranking[i] += freq[w] #adding importance
            
#four most important sentences
sents_idx = nlargest(4, ranking, key=ranking.get)
            
final = "".join([sent[j] for j in sorted(sents_idx)])

