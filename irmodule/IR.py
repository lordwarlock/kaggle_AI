#!/usr/bin/env python
#encoding:utf8
from whoosh.index import create_in
from whoosh.fields import *
from whoosh.qparser import QueryParser
from FileProcess import *
class IR():
    def __init__(self,filePath,indexPath):
        schema =Schema(title=TEXT(stored=True),path=ID(stored=True),content=TEXT(stored=True))
        self.ix=create_in(indexPath,schema)
        self.filePath=filePath
    def CreateIndex(self):
        writer =self.ix.writer()
        data=readWikipedia(self.filePath)
        for item in data:
            writer.add_document(title=item['title'].decode("utf-8"),path=u"/a",content=item["content"].decode("utf-8"))
        writer.commit()
        print "index finished"
    
    def Search(self,query):
        with self.ix.searcher() as searcher:
            query= QueryParser("content",self.ix.schema).parse(query)
	    results=searcher.search(query)
            print results[0]
            return results


if __name__=="__main__":
    print "start"
    ir=IR("top1000.xml","./index/")
    ir.CreateIndex()
    ir.Search(u"autistic symptoms")
