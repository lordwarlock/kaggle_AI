#!/usr/bin/env python
#encoding:utf8
import xml.etree.ElementTree as et
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

if __name__=="__main__":
    readWikipedia("top1000.xml")

