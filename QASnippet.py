# -*- coding: utf-8  -*-
from __future__ import unicode_literals
import codecs
from nltk.tokenize import sent_tokenize
from nltk import word_tokenize

class QASnippet(object):
    def __init__(self): pass

    def article_to_tokenized_sentences(self,raw_article):
        sentences = sent_tokenize(raw_article)
        return [ word_tokenize(sentence) for sentence in sentences]

    def similarity(self, sentence, qa): pass
        
if __name__ == '__main__':
    with codecs.open('test_article.txt',mode='r',encoding='utf-8') as fin:
        for x in QASnippet().article_to_tokenized_sentences(fin.read()):
            print x
            print '----------------------------'
