import re
from concurrent.futures import ThreadPoolExecutor,as_completed
from urllib.request import Request,urlopen
from urllib.parse import urlparse,urljoin
from .budget import Budget
from .evidence import make_finding
from .scope import require_target,require_path
def title(body):
 m=re.search(r'<title[^>]*>(.*?)</title>',body[:10000],re.I|re.S)
 return re.sub(r'\s+',' ',m.group(1)).strip() if m else None
def scan(s,base,words):
 p=urlparse(base); require_target(s,p.hostname or '')
 if p.scheme not in ('http','https'):raise ValueError('only http and https are supported')
 b=Budget(s.max_requests,s.max_connections,s.min_delay_ms)
 def one(w):
  path='/'+w.strip().lstrip('/'); require_path(s,path); url=urljoin(base.rstrip('/')+'/',path.lstrip('/')); b.request()
  try:
   req=Request(url,method='GET',headers={'User-Agent':s.user_agent,'X-Contact':s.contact})
   with urlopen(req,timeout=4) as r:
    body=r.read(16384); ct=r.headers.get('Content-Type',''); st='interesting' if r.status in (200,204,301,302,401,403) else 'not_found'; ev={'http_status':r.status,'content_type':ct,'content_length':len(body),'title':title(body.decode('utf-8','replace')) if 'text' in ct else None}; return make_finding('paths',url,st,'medium' if st=='interesting' else 'low',ev,'GET','Discovery is not proof of authorization bypass.')
  except Exception as e:return make_finding('paths',url,'error','low',{'error':type(e).__name__},'GET')
 with ThreadPoolExecutor(max_workers=s.max_concurrency) as pool:return [x.result() for x in as_completed([pool.submit(one,w) for w in words if w.strip()])]
