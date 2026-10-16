import re, sys, json, os, urllib.request, urllib.parse, ssl, hashlib
from html.parser import HTMLParser
BASE='https://globalwms.com'
OUT=sys.argv[1]
os.makedirs(OUT+'/pages',exist_ok=True); os.makedirs(OUT+'/files',exist_ok=True)
ctx=ssl.create_default_context(cafile='/root/.ccr/ca-bundle.crt')
def get(u):
    req=urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0 (audit)'})
    class NR(urllib.request.HTTPRedirectHandler):
        def redirect_request(s,*a,**k): return None
    op=urllib.request.build_opener(NR,urllib.request.HTTPSHandler(context=ctx))
    try:
        r=op.open(req,timeout=30); return r.status,{k.lower():v for k,v in r.headers.items()},r.read()
    except urllib.error.HTTPError as e:
        return e.code,{k.lower():v for k,v in e.headers.items()},e.read()
    except Exception as e:
        return 0,{'err':str(e)},b''
class P(HTMLParser):
    def __init__(s): super().__init__(); s.l=[]
    def handle_starttag(s,t,a):
        a=dict(a)
        for k in ('href','src','data-src','data-fancybox-href','poster'):
            if a.get(k): s.l.append((t,k,a[k]))
        if a.get('style'):
            for m in re.findall(r'url\(([^)]+)\)',a['style']): s.l.append((t,'style',m.strip('\'"')))
seen={};queue=['/'];assets={}
while queue:
    p=queue.pop(0)
    if p in seen: continue
    st,h,b=get(BASE+p)
    ct=h.get('content-type','')
    seen[p]={'status':st,'type':ct,'loc':h.get('location'),'size':len(b)}
    if st in(301,302,303,307,308) and h.get('location'):
        loc=urllib.parse.urljoin(BASE+p,h['location'])
        if loc.startswith(BASE): queue.append(loc[len(BASE):] or '/')
        continue
    if st!=200: continue
    fn=OUT+'/pages/'+hashlib.md5(p.encode()).hexdigest()[:8]+'.html'
    if 'html' in ct:
        open(fn,'wb').write(b); seen[p]['file']=fn
        pr=P(); pr.feed(b.decode('utf8','replace'))
        for t,k,v in pr.l:
            if v.startswith(('mailto:','tel:','javascript:','#','data:')): continue
            u=urllib.parse.urljoin(BASE+p,v).split('#')[0]
            if not u.startswith(BASE): assets.setdefault(u,set()).add(p); continue
            path=u[len(BASE):] or '/'
            assets.setdefault(u,set()).add(p)
            if t=='a' and k=='href' : queue.append(path)
            elif re.search(r'\.(pdf|docx?|xlsx?|pptx?|zip)(\?|$)',path,re.I): queue.append(path)
json.dump(seen,open(OUT+'/pages.json','w'),indent=1)
json.dump({k:sorted(v) for k,v in assets.items()},open(OUT+'/refs.json','w'),indent=1)
for p,v in seen.items(): print(v['status'],v['type'][:20],p,v.get('loc') or '')
