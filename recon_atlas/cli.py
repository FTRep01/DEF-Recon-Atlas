import argparse,json,uuid
from pathlib import Path
from .config import load_scope,scope_hash
from .scope import validate_scope,enforce_window
from .dns import resolve
from .ports import scan as port_scan
from .http_paths import scan as path_scan
from .subdomains import from_wordlist
from .reports import write_report
from .models import Run
def main(argv=None):
 p=argparse.ArgumentParser(prog='recon-atlas'); sub=p.add_subparsers(dest='cmd',required=True)
 i=sub.add_parser('init-scope'); i.add_argument('--domain',required=True); i.add_argument('--out',required=True)
 v=sub.add_parser('validate-scope'); v.add_argument('--scope',required=True)
 d=sub.add_parser('subdomains'); d.add_argument('--scope',required=True); d.add_argument('--wordlist',required=True); d.add_argument('--mode',choices=('passive','active'),default='passive'); d.add_argument('--out',required=True)
 o=sub.add_parser('ports'); o.add_argument('--scope',required=True); o.add_argument('--host',required=True); o.add_argument('--out',required=True)
 h=sub.add_parser('paths'); h.add_argument('--scope',required=True); h.add_argument('--url',required=True); h.add_argument('--wordlist',required=True); h.add_argument('--out',required=True)
 s=sub.add_parser('scan'); s.add_argument('--scope',required=True); s.add_argument('--module',choices=('dns','ports','paths','all'),default='all'); s.add_argument('--host'); s.add_argument('--url'); s.add_argument('--wordlist',default='data/paths.txt'); s.add_argument('--out',required=True)
 r=sub.add_parser('report'); r.add_argument('--input',required=True); r.add_argument('--format',choices=('json','csv','markdown','html'),required=True); r.add_argument('--out',required=True)
 a=p.parse_args(argv)
 if a.cmd=='init-scope':
  x={'scope_id':'replace-me','operator':'security@example.com','authorized_by':'owner@example.com','valid_from':'2026-01-01T00:00:00Z','valid_until':'2026-12-31T23:59:59Z','domains':[a.domain],'hosts':[],'cidrs':[],'ports':[80,443],'path_prefixes':['/','/robots.txt','/sitemap.xml'],'max_requests':100,'max_connections':50,'min_delay_ms':500,'max_concurrency':2,'allow_private':False,'contact':'security@example.com','user_agent':'ReconAtlas/0.1 (+security@example.com)'}; Path(a.out).write_text(json.dumps(x,indent=2)+'\n'); print('scope template written:',a.out); return 0
 if a.cmd=='report':write_report(json.loads(Path(a.input).read_text()),a.format,a.out); return 0
 s=load_scope(a.scope); errs=validate_scope(s)
 if errs:print(json.dumps({'valid':False,'errors':errs},indent=2));return 2
 if a.cmd=='validate-scope':print(json.dumps({'valid':True,'scope_id':s.scope_id,'scope_sha256':scope_hash(s)},indent=2));return 0
 enforce_window(s); findings=[]
 if a.cmd=='subdomains':findings=from_wordlist(s,a.wordlist,a.mode)
 elif a.cmd=='ports':findings=port_scan(s,a.host)
 elif a.cmd=='paths':findings=path_scan(s,a.url,Path(a.wordlist).read_text().splitlines())
 elif a.cmd=='scan':
  if a.module in ('all','dns'):
   for d in s.domains:findings+=resolve(s,d)
  if a.module in ('all','ports') and a.host:findings+=port_scan(s,a.host)
  if a.module in ('all','paths') and a.url:findings+=path_scan(s,a.url,Path(a.wordlist).read_text().splitlines())
 run=Run('run-'+uuid.uuid4().hex[:12],__import__('datetime').datetime.now(__import__('datetime').timezone.utc).isoformat(),s.scope_id,scope_hash(s),[a.cmd],[x.to_dict() for x in findings],{'finding_count':len(findings),'max_concurrency':s.max_concurrency},[])
 Path(a.out).parent.mkdir(parents=True,exist_ok=True);Path(a.out).write_text(json.dumps(run.to_dict(),indent=2,ensure_ascii=False)+'\n',encoding='utf-8');print('wrote',len(findings),'findings to',a.out);return 0
if __name__=='__main__':main()
