homepath='../'
subfolder=[]
exclude=['../404.html']
redirect={'../Publication.html':None,
'../Publication_en.html':'../reuse/publist.html',
}

outputpath='./tipuesearch_content.js'

import os
import re
from bs4 import BeautifulSoup
import json
title_patt=re.compile(r"<title>(.*?)</title>")


def dealall():
    sub=[homepath+k for k in subfolder]
    allnode=[]
    for item in [homepath]+sub:
        html_list=[item+k for k in os.listdir(item) if '.html' in k]
        for html in html_list:
            if html in exclude:
                print("不处理"+html)
            elif html in redirect and redirect[html] == None:
                print("不处理"+html)
            else:
                allnode.append(deal_html(html))
                
    root_node = {'pages': allnode}
    root_node_js = 'var tipuesearch = ' + json.dumps(root_node, separators=(',', ':'), ensure_ascii=False) + ';'
    with open(outputpath, 'w+', encoding='utf-8') as fd:
        fd.write(root_node_js)

def deal_html(html):
    if html in redirect:
        print("正在处理"+html)
        with open(html,'r+',encoding='utf8') as f:
            content=f.read()
        page_title=re.findall(title_patt,content)[0]
        page_url=html.replace(homepath,'')
        with open(redirect[html],'r+',encoding='utf8') as f:
            content=f.read()
        soup_text=BeautifulSoup(content, 'html.parser')  
    else:
        print("正在处理"+html)
        page_url=html.replace(homepath,'')
        with open(html,'r+',encoding='utf8') as f:
            content=f.read()
        page_title=re.findall(title_patt,content)[0]
        soup_text=BeautifulSoup(content, 'html.parser')
        
    page_title=page_title.replace('“', '"').replace('”', '"').replace('’', "'").replace('^', '&#94;')
    page_title=page_title.replace('☰',' ')
    page_text=soup_text.get_text(' ', strip=True).replace('“', '"').replace('”', '"').replace('’', "'").replace('¶', ' ').replace('^', '&#94;')
    page_text=page_text.replace('☰',' ')
    page_text = ' '.join(page_text.split())
    node = {'title': page_title,
    'text': page_text,
    'tags': "",
    'loc': page_url
    }
    return node

if __name__ =="__main__":
    dealall()