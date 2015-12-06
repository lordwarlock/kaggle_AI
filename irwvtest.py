'''
@author: Kechen
'''
from gensim.models import word2vec
import logging
from nltk.corpus import stopwords
from threading import Thread
import functools
import sys
import multiprocessing
import Queue
import wikipedia
from nltk.tag import pos_tag
import time
import re
import string
from threading import *
from scipy import spatial
import numpy as np
import sqlite3
from bs4 import BeautifulSoup
import multiprocessing as mp
import urllib2
from datetime import timedelta, datetime
from time import sleep
from nltk.tokenize import word_tokenize
import pandas as pd
from QuestionAnswer import QuestionAnswerList

class Util():
    def _get_wikicontent(self, keyword):
        '''download wiki, if cannot find this keyword, return noresult'''
        try: 
            result = wikipedia.page(keyword)
        except:
            print 'noresult'
            return ''
        c= result.content
        c= str(c.decode('utf-8'))
        
        return c
    
    def _get_nnp(self, sentence):
        '''get proper nouns'''
        tagged_sent = pos_tag(sentence.split())
        propernouns = [word for word,pos in tagged_sent if pos == 'NNP']
        regex = re.compile('[^a-zA-Z]')
        propernouns = [regex.sub('', i) for i in propernouns]
        return propernouns 
    
    def _get_nn(self, sentence):
        '''get proper nouns'''
        tagged_sent = pos_tag(sentence)
        propernouns = [word for word,pos in tagged_sent if pos == 'NN']
        regex = re.compile('[^a-zA-Z]')
        propernouns = [regex.sub('', i) for i in propernouns]
        return propernouns
    
    def _remove_stop_words(self, sentence):
#        word_list = word_tokenize(sentence.decode('ISO-8859-1'))
        filtered_words = [word for word in sentence if word not in stopwords.words('english')]
        return filtered_words

class DBConnection():
    def __init__(self):
        self.conn = sqlite3.connect('H:\machine learning\AI science\google_vec.db')
        self.c = self.conn.cursor()
    
    def _get_vec(self, keyword):
#        return self.c.execute("select * from word_vector where word='"+keyword+"' COLLATE NOCASE").fetchone()
        print 'start'
        return list(self.c.execute("select * from word_vector where word='"+keyword+"' COLLATE NOCASE").fetchone())[1:]
        print 'end'
        
    
    def cal_simi(self, word1, word2):
        vec1 = self._get_vec(word1)
        vec2 = self._get_vec(word2)
        distance = 1 - spatial.distance.cosine(vec1, vec2)
        
        return distance

class W2V():
    def __init__(self):
        logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
#        self.model = word2vec.Word2Vec.load(r'G:/global impact rating/enwik9model') 
        self.model = word2vec.Word2Vec.load_word2vec_format(r'G:\global impact rating\GoogleNews-vectors-negative300.bin', binary=True)
         
    def cal_simi(self, word1, word2):
        if word1 in self.model.vocab and word2 in self.model.vocab:
            return self.model.similarity(word1, word2)
        else:
            return 0   
             
if __name__ == '__main__':
    dic = {0:'A', 1:'B', 2:'C', 3:'D'}
    result_list = []
    utility = Util()
    dbcon = W2V()
    
    f=open('testresult3.txt', 'a')
#    print dbcon._get_vec('store')
#    print dbcon.cal_simi('sun', 'hero')
#        return None
    reload(sys)  # Reload does the trick!
    sys.setdefaultencoding("utf-8")
    qa_list = QuestionAnswerList(r'H:\machine learning\AI science\validation_set.tsv')
    index=0
    for i in  qa_list.qa_list:
        question = i.question
        question = utility._get_nn(question)
        question = [''.join(c for c in s if c not in string.punctuation) for s in question]
        question = [s for s in question if s]
        answer_list = i.answer_list
        nnp_list=[]
        for word in question:
            wiki_content = utility._get_wikicontent(word)
            wiki_nnp = utility._get_nnp(wiki_content)
            wiki_nnp = utility._remove_stop_words(wiki_nnp)  # remove stop words.
            nnp_list = nnp_list+wiki_nnp
        answer_score = []
        for answer in answer_list:
            answer_length = len(answer)
            tmp_score=0
            for word in answer:
                for nnp in nnp_list:
                    cos = dbcon.cal_simi(nnp, word)
                    if cos>0.3:
                        tmp_score = tmp_score+1
            answer_score.append(tmp_score)
        
        print answer_score
        z=np.array(answer_score)
        result_list.append(dic[np.argmax(z)])
        print dic[np.argmax(z)]
        f.write(dic[np.argmax(z)]+'\n')
        f.flush()
#    with open('testresult.txt', 'a') as f:
#        for ans in result_list:
#            f.write(ans+'\n')
    f.close()
    print result_list
