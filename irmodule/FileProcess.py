#!/usr/bin/env python
#encoding:utf8
import xml.etree.ElementTree as et
def readWikipedia(filePath,namespace="{http://www.mediawiki.org/xml/export-0.10/}",
                  parent="page",title="title",content="text"):
    #in case of out of memory error,please split large file into small chunks
    #file should be in format of xml
    root=et.parse(filePath).getroot()
    pages=root.findall(namespace+parent)
    dictRes=[]
    for page in pages:
        tmp=dict()
        tmp["title"]= page.find(namespace+title).text
        print type(tmp["title"])
        tmp["content"]=page.find(namespace+content).text
        dictRes.append(tmp)
    print len(dictRes)
    return dictRes

if __name__=="__main__":
    readWikipedia("top1000.xml")

