#!/usr/bin/env python
#encoding:utf8
import xml.etree.ElementTree as et
from itertools import takewhile, chain
from bs4 import BeautifulSoup,BeautifulStoneSoup
import urllib2
import re
import glob
import codecs
import os

def readWikipedia(filePath,namespace="{http://www.mediawiki.org/xml/export-0.10/}"):
    #in case of out of memory error,please split large file into small chunks
    #file should be in format of xml
    root=et.parse(filePath).getroot()
    pages=root.findall(namespace+"page")
    dictRes=[]
    for page in pages:
        tmp=dict()
        title=page.find(namespace+"title")
        tmp["title"]= title.text.encode('utf-8')
        content=page.find(namespace+"revision").find(namespace+"text")
        tmp["content"]=content.text.encode('utf-8')
        print tmp["title"]
        dictRes.append(tmp)
    print len(dictRes)
    return dictRes

def buildindexCK12():
    dictRes=[]
    deletelist = ['Explore More', 'References', 'Practice']
    for f in glob.glob(r'H:\machine learning\AI science\ck_text\*.txt'):
        colname = os.path.basename(os.path.splitext(f)[0])
        print colname
        f1 = open(f,'r')
        flag = True
        index = 0
        content = ''
        title = ''
        dic = {}
        for line in f1:
            line = line.strip()
            if line=='\n' or line=='' or line=='':
                continue
            if flag:
                titles = eval(line)
                flag = False
                continue
            if index<len(titles) and unicode(titles[index],"utf-8")==line:
                if title is not '':
                    dic['title'] = title
                    dic['content'] = content
                    dictRes.append(dic)
                index+=1
                print line
                title = line
                content = ''
                dic = {}
            content = content+' '+line
            
        dic['title'] = title
        dic['content'] = content
        dictRes.append(dic)
        f1.close()
    
    dictRes = [i for i in dictRes if i['title'] not in deletelist]
    print len(dictRes)
    return dictRes

def readCK12(filePath):
    soup=BeautifulSoup(open(filePath),"lxml")
#    x=soup.find_all('h1', id=re.compile('calibre_link-*.*'), class_='calibre10')
    tmp = soup.find_all('div', id=re.compile('calibre_link-*'), class_='calibre')
    for i in xrange(2, len(tmp)):
        titles = tmp[i].find_all(re.compile('h.*'), id=re.compile('calibre_link-.*'), class_=re.compile('calibre.*'))
        titles = [t.getText().replace(r'\n', '').strip().encode('utf-8') for t in titles]
        main_text = tmp[i].getText().encode('utf-8')
        f = open('H:\machine learning\AI science\ck_text\\'+str(titles[0]).replace('?', '').replace(':', '')+'.txt', 'w')
#        f2 = open('H:\machine learning\AI science\ck_html\\'+str(titles[0]).replace('?', '').replace(':', '')+'.txt', 'w')
        f.write(str(titles)+'\n'+main_text)
#        f2.write(str(tmp[i]))
        f.close()

if __name__=="__main__":
    buildindexCK12()
#    readCK12(r'H:\machine learning\AI science\Concepts - CK-12 Foundationunzip\index.html')
