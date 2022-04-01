#默认bib文件已按照时间顺序排列
import bibtexparser
from deal_bib import *
import time
import re
from tkinter import messagebox

start=time.localtime().tm_year
end=2016

def readbib(bibpath):
    '''读取bib文件，并将month格式化'''
    #读取文件
    with open(bibpath,'r+',encoding='utf8') as f:
        tmp=f.read()
    #bibtex文件的month格式不加{}，导致报错
    #month    = may,变为month    = {may},
    patt_month=r'month(\s*?)=(\s*?)([a-z]{3})'
    tmp=re.sub(patt_month,lambda m:'month'+m.group(1)+'='+m.group(2)+'{'+m.group(3)+'}',tmp)
    biball=bibtexparser.loads(tmp)
    return biball

def dictbib(biball):
    '''将bib的所有条目变为时间戳对应的字典'''
    entry_dict={}
    timestamp=[]
    for item in biball.entries:
        _tmp=int(item['note'])
        timestamp.append(_tmp)
        entry_dict.update({_tmp:item})
    set_time=set(timestamp)
    if len(set_time)==len(timestamp):
        timestamp.sort(reverse=True)
        return timestamp,entry_dict
    else:
        return None,None

def main(origin,des):
    '''主函数，生成HTML'''
    category='<tr><th class="pubyear">yearcategory</th></tr>'
    html='<table class="table">\n'
    htmlyear=0
    stop=False
    biball=readbib(bibpath=origin)
    timestamp,entry_dict=dictbib(biball)
    if timestamp==None:
        messagebox.showerror('note域重复，请检查')
    else:
        for item in timestamp:
            bib=entry_dict[item]
            year=int(bib['year'])
            if year>end-1 and year!=htmlyear:
                newcategory=category.replace('yearcategory',bib['year'])+'\n\n'
                html=html+newcategory
                htmlyear=year
            elif not stop and year<=end-1:
                tmp=str(end)+'年之前'
                newcategory=category.replace('yearcategory',tmp)+'\n\n'
                html=html+newcategory
                stop=True
            else:
                pass
            newitem=formatitem(bib)
            html=html+newitem+'\n\n'
        html=html+'</table>'
        with open(des,'w+',encoding='utf8') as f:
            f.write(html)

if __name__=='__main__':
    origin='./lilab.bib'
    des='../publist.html'
    main(origin,des)

#旧版所用，新版不再需要
# monlist=['jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec']
'''
#旧版
for i in range(start,end-1,-1):
    years=str(i)
    newcategory=category.replace('yearcategory',years)+'\n'
    html=html+newcategory
    for bib in biball.entries:
        if bib['year']==years:
            newitem=formatitem(bib)
            html=html+newitem+'\n\n'
html=html+'</table>'
with open('./pypublist.html','w+',encoding='utf8') as f:
    f.write(html)
'''
