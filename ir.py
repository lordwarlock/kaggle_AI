#coding:utf8
from whoosh.index import create_in
from whoosh.fields import *
schema =Schema(title=TEXT(stored=True),path=ID(stored=True),content=TEXT)
ix=create_in(u"./index/",schema)
writer =ix.writer()
writer.add_document(title=u"first document",path=u"/a",
	content=u"This is the first document")
writer.add_document(title=u"second document",path=u"/a",
	content=u"This is the second document,is even more interesting")
writer.commit()

from whoosh.qparser import QueryParser
with ix.searcher() as searcher:
	query= QueryParser("content",ix.schema).parse("first")
	results=searcher.search(query,scored=True)
	print results.score(0)
