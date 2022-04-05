import bibtexparser
import re
pattern1=re.compile(r'\$_{(.+?)}\$')
pattern2=re.compile(r'\$\^{(.+?)}\$')
html_escape_table = {
    '&': '&amp;',
    '--':'–',
    '"': '&quot;',
    "'": '&apos;',
    '\\alpha':'α','\\beta':'β','\\gamma':'γ','\\delta':'δ','\\epsilon':'ϵ','\\varepsilon':'ε',
    '\\zeta':'ζ','\\eta':'η','\\theta':'θ','\\iota':'ι','\\kappa':'κ','\\lambda':'λ','\\mu':'μ',
    '\\nu':'ν','\\xi':'ξ','\\omicron':'ο','\\pi':'π','\\rho':'ρ','\\sigma':'σ','\\tau':'τ',
    '\\upsilon':'υ','\\phi':'ϕ','\\varphi':'φ','\\chi':'χ','\\psi':'ψ',
    '{':'','}':'',
    }
paper='<tr><td class="paperlist">order. <a href="doiurl" target="_blank">papertitle</a><br/>paperauthor<br/>source</b><button data-toggle="collapse" data-target="#bibkey" type="button" class="mybtn btn-link">bib</button><div id="bibkey" class="collapse bibtex">bibinfo</div>  </td></tr>'


def change(text):
    '''替换上下标'''
    tmp=re.sub(pattern1,lambda m:'<sub>'+m.group(1)+'</sub>',text)
    tmp=re.sub(pattern2,lambda m:'<sup>'+m.group(1)+'</sup>',tmp)
    for item in html_escape_table:
        tmp=tmp.replace(item,html_escape_table[item])
    return tmp

def gettitle(bib):
    '''获取标题'''
    title=change(bib['title'])
    #title=[html_escape_table.get(c,c) for c in title]
    title=''.join(title)
    return title

def getauthor(bib):
    '''获取作者'''
    author=bib['author'].split(' and ')
    for i in range(len(author)):
        tmp=author[i]
        tmp=tmp.split(', ')
        author[i]=tmp[1]+' '+tmp[0]
    author='Author(s): '+', '.join(author)
    return author

def getsource(bib):
    '''获取出版信息'''
    if bib['ENTRYTYPE'].lower()=='article':
        #文献类型为article时
        pages=bib['pages'].replace('--','–')
        try:
            number=' ('+bib['number']+')'
        except:
            number=''
        source='Source: <b><i>'+bib['journal']+'</i>, '+bib['volume']+number+', '+pages+', '+bib['year']+'.</b>'
    elif bib['ENTRYTYPE'].lower()=='inproceedings':
        #文献类型为inproceedings时
        source='Source: <b><i>'+bib['booktitle']+'</i>, '+bib['year']+'.</b>'
    elif bib['ENTRYTYPE'].lower()=='misc':
        #文献类型为misc时，这里用misc指代已接收无DOI文章
        source='Source: <b><i>'+bib['howpublished']+'</i>, '+bib['year']+', accepted.</b>'
    return source+'&nbsp;'

def getbibinfo(bib):
    '''去除misc的输出'''
    exclued_field=['groups','ENTRYTYPE','ID','note','category','file','abstract']
    if bib['ENTRYTYPE'].lower()=='misc':
        return "暂无bib"
    else:
        bibinfo='@'+bib['ENTRYTYPE']+'{'+bib['ID']+',</br>\n'
        for item in bib:
            if item not in exclued_field:
                bibinfo=bibinfo+item+'={'+bib[item]+'},</br>\n'
        return bibinfo+'}'

def getdoiurl(bib):
    if bib['ENTRYTYPE'].lower()=='misc':
        #文献类型为misc时，这里用misc指代已接收无DOI文章
        return '#'
    else:
        return 'https://doi.org/'+bib['doi']
    
#paper='<tr><td class="paperlist">order. <a href="doiurl" target="_blank">papertitle</a><br/>paperauthor<br/>source</b><button data-toggle="collapse" data-target="#bibkey" type="button" class="mybtn btn-link">bib</button><div id="bibkey" class="collapse bibtex">bibinfo</div>  </td></tr>'
def formatitem(bib,order):
    '''获取格式化输出'''
    print('正在处理第%d个文献'%order)
    bibkey=bib['ID']
    tmp=paper.replace('order',str(order))
    tmp=tmp.replace('doiurl',getdoiurl(bib))
    tmp=tmp.replace('papertitle',gettitle(bib))
    tmp=tmp.replace('paperauthor',getauthor(bib))
    tmp=tmp.replace('source',getsource(bib))
    tmp=tmp.replace('bibkey',bibkey)
    tmp=tmp.replace('bibinfo',getbibinfo(bib))
    return tmp
    