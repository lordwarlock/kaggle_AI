#!/usr/bin/env python
#encoding:utf8
from whoosh.index import create_in
import os
from whoosh.fields import *
from whoosh.qparser import QueryParser
from FileProcess import *
from whoosh.index import open_dir
from wikipedia import Wikipedia
from wiki2plain import Wiki2Plain

class IR():
    def __init__(self,indexPath,isRead=False):
        schema =Schema(title=TEXT(stored=True),path=ID(stored=True),content=TEXT(stored=True))
        if isRead:
            self.ix=open_dir(indexPath)
        else:
            self.ix=create_in(indexPath,schema)

    def CreateIndex(self,data):
        writer =self.ix.writer()
        for item in data:
            writer.add_document(title=item['title'].decode("utf-8"),path=u"/a",content=item["content"].decode("utf-8"))
        writer.commit()

    def dirlist(self,path, allfile):
        if os.path.isfile(path):
            allfile.append(path)
            return allfile
	filelist =  os.listdir(path)
        for filename in filelist:
            filepath = os.path.join(path, filename)
            if os.path.isdir(filepath):
                self.dirlist(filepath, allfile)
            else:
                allfile.append(filepath)
        return allfile

    def addIndexForWiki(self,filePath):
        allfile=self.dirlist(filePath,[])
        for efile in allfile:
            print efile
            self.CreateIndex(readWikipedia(efile))
        print "index finished"

    def Search(self,query):
        title_list = []
        content_list = []
        score_list = []
        with self.ix.searcher() as searcher:
            query= QueryParser("content",self.ix.schema).parse(query)
            results=searcher.search(query)
            index=0
            for i in results:
                #print i
                title_list.append(i["title"])
                content_list.append(i["content"])
                score_list.append(results.score(index))
                index += index
            #for score, you can use results.score(i) to get the score.
            return title_list, content_list, score_list

    
    def wiki_parser(self, raw):
        wiki2plain = Wiki2Plain(raw)
        return wiki2plain.text
    
    def wiki_clean(self, text):
        text = self.wiki_parser(text)
        list = text.split('\n')
        list = [i for i in list if '==' not in i]
        list = [i for i in list if len(i.split(':'))!=2]
        print ' '.join(list)
        
if __name__=="__main__":
    #add index:
    isRead=False
    ir=IR("./index",isRead)    
    #if wiki data, you can just pass the dir name or file name for  function addIndexForWiki
    ir.addIndexForWiki('./data/')
    #if for ck12 data
    ir.CreateIndex(buildindexCK12())#default path r'./ck_text/*.txt'

   #if wiki
   # print "start"
   # ir=IR(r"H:\machine learning\AI science\kaggle_AI-master\irmodule\data","./index/",True)
    search_result = ir.Search('april')
    title_list = search_result[0]
    content_list = search_result[1]
    score_list = search_result[2]
    print len(search_result)
    print title_list
    #for i in title_list:
     #   print i
   # 
   # ir.wiki_clean(content_list[0])
