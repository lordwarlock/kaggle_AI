#!/usr/bin/env python
#encoding:utf8
from whoosh.index import create_in
import os
from whoosh.fields import *
from whoosh.qparser import QueryParser
from FileProcess import *
from whoosh.index import open_dir
class IR():
    def __init__(self,filePath,indexPath,isRead=False):
        schema =Schema(title=TEXT(stored=True),path=ID(stored=True),content=TEXT(stored=True))
        self.filePath=filePath
        if isRead:
            self.ix=open_dir(indexPath)
        else:
            self.ix=create_in(indexPath,schema)
            self.addIndex(filePath)

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
                dirlist(filepath, allfile)
            else:
                allfile.append(filepath)
        return allfile

    def addIndex(self,filePath):
        allfile=self.dirlist(filePath,[])
        for efile in allfile:
            print efile
            self.CreateIndex(readWikipedia(efile))
        print "index finished"

    def Search(self,query):
        with self.ix.searcher() as searcher:
            query= QueryParser("content",self.ix.schema).parse(query)
	    results=searcher.search(query)
            print results[0]["title"]
            #for score, you can use results.score(i) to get the score.
            print results.score(0)
            return results


if __name__=="__main__":
    print "start"
    ir=IR("data","./index/",False)
    ir.Search(u"autistic symptoms")
