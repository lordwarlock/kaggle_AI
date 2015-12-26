#encoding:utf8
import xml.etree.ElementTree as et
from itertools import takewhile, chain
from bs4 import BeautifulSoup,BeautifulStoneSoup
import urllib2
import re
import glob
import codecs
import os
import wikipedia
from urllib2 import urlopen
from wiki2plain import Wiki2Plain


def wiki_parser(raw):
    wiki2plain = Wiki2Plain(raw)
    return wiki2plain.text

def wiki_clean(text):
    text = wiki_parser(text)
    list = text.split('\n')
    list = [i for i in list if '==' not in i]
    list = [i for i in list if len(i.split(':')[0].split())!=1]
    return ' '.join(list)

def readWikipedia(filePath,namespace="{http://www.mediawiki.org/xml/export-0.4/}"):
    #in case of out of memory error,please split large file into small chunks
    #file should be in format of xml
    root=et.parse(filePath).getroot()
    pages=root.findall(namespace+"page")
    print pages
    dictRes=[]
    for page in pages:
        tmp=dict()
        title=page.find(namespace+"title")
        tmp["title"]= title.text.encode('utf-8')
        content=page.find(namespace+"revision").find(namespace+"text")
        if content.text is None:
            continue 
#        tmp["content"]=content.text.encode('utf-8')
        tmp["content"]=wiki_clean(content.text.encode('utf-8'))
        print tmp["title"]
        dictRes.append(tmp)
    print len(dictRes)
    return dictRes

def buildindexCK12(file_path):
    dictRes=[]
    deletelist = ['Explore More', 'References', 'Practice']
    for f in glob.glob(file_path+'\*.txt'):
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
                    dic['title'] = titles[0]+':'+title
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
        

def get_save_wiki_docs(keywords, save_folder):
    n_total = len(keywords)
    for i, kw in enumerate(keywords):
        try: 
            result = wikipedia.page(kw)
        except:
            print 'noresult'
            continue
        c= result.content
        c= str(c.decode('utf-8'))
        filename = save_folder + kw + '.txt'
        print filename
        with open(filename, 'w') as f:
            f.write(c)
    
ck12_url_topic = ['https://www.ck12.org/earth-science/', 'http://www.ck12.org/life-science/', 
              'http://www.ck12.org/physical-science/', 'http://www.ck12.org/biology/', 
              'http://www.ck12.org/chemistry/', 'http://www.ck12.org/physics/']

wiki_docs_dir = 'H:\machine learning\AI science\ck_wiki\\'  # address of ck_wiki

def get_keyword_from_url_topic(url_topic):
    # Topic includes: Earth Science, Life Science, Physical Science, Biology, Chemestry and Physics
    lst_url = []
    html = urlopen(url_topic).read()
    soup = BeautifulSoup(html, 'html.parser')
    for tag_h3 in soup.find_all('h3'):
        url_res =  ' '.join(tag_h3.li.a.get('href').strip('/').split('/')[-1].split('-'))
        lst_url.append(url_res)
    return lst_url

def get_wiki_docs():
    # get keywords 
    ck12_keywords = set()
    for url_topic in ck12_url_topic:
        keywords= get_keyword_from_url_topic(url_topic)
        for kw in keywords:
            print kw
            ck12_keywords.add(kw)
    
    #get and save wiki docs
    get_save_wiki_docs(ck12_keywords, wiki_docs_dir)
    
def _get_wikicontent(keyword):
    '''download wiki, if cannot find this keyword, return noresult'''
    try: 
        result = wikipedia.page(keyword)
    except:
        print 'noresult'
        return ''
    c= result.content
    c= str(c.decode('utf-8'))
    
    return c

def create_CKWiki_index(foldername):
    dictRes = []
    for f in glob.glob(foldername+'\*.txt'):
        colname = os.path.basename(os.path.splitext(f)[0])
        print colname
        f1 = open(f,'r')
        content = f1.read()
        f1.close()
        dic = {}
        dic['title'] = colname
        dic['content'] = content
        dictRes.append(dic)
    
    return dictRes
            
    
if __name__=="__main__":
#    buildindexCK12()
    readCK12(r'H:\machine learning\AI science\Concepts - CK-12 Foundationunzip\index.html')
    get_wiki_docs()
#    create_CKWiki_index('H:\machine learning\AI science\ck_wiki')
