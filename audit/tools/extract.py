import json,re,sys,html
pages=json.load(open('raw/crawl/pages.json'))
for p,v in pages.items():
    if 'file' not in v: continue
    h=open(v['file'],encoding='utf8').read()
    g=lambda rx:(re.search(rx,h,re.S|re.I) or [None,None])[1]
    t=g(r'<title>(.*?)</title>'); d=g(r'<meta name="description" content="(.*?)"'); c=g(r'<link rel="canonical" href="(.*?)"')
    kw=g(r'<meta name="keywords" content="(.*?)"'); rb=g(r'<meta name="robots" content="(.*?)"')
    m=re.search(r'<main.*?</main>',h,re.S)
    body=m.group(0) if m else ''
    txt=re.sub(r'<(script|style).*?</\1>','',body,flags=re.S)
    txt=re.sub(r'</(p|h\d|li|tr|div|table|ul)>','\n',txt); txt=re.sub(r'<br\s*/?>','\n',txt)
    txt=html.unescape(re.sub(r'<[^>]+>','',txt)); txt=re.sub(r'[ \t]+',' ',txt); txt=re.sub(r'\n\s*\n+','\n',txt)
    print('='*100);print(p,'| TITLE:',t,'| DESC:',d,'| CANON:',c,'| KW:',kw,'| ROBOTS:',rb,'| bytes',len(body),'| words',len(txt.split()))
    v.update(title=t,desc=d,canon=c)
    if '-v' in sys.argv: print(txt)
json.dump(pages,open('raw/crawl/pages.json','w'),indent=1)
