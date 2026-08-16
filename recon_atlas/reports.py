import csv,html,io,json
from pathlib import Path
def write_report(run,fmt,out):
 rows=run.get('findings',[]); p=Path(out); p.parent.mkdir(parents=True,exist_ok=True)
 if fmt=='json':p.write_text(json.dumps(run,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
 elif fmt=='csv':
  b=io.StringIO(); f=['finding_id','module','target','status','confidence','method','observed_at']; w=csv.DictWriter(b,fieldnames=f); w.writeheader(); w.writerows({k:r.get(k) for k in f} for r in rows); p.write_text(b.getvalue(),encoding='utf-8')
 elif fmt=='markdown':p.write_text('# Recon Atlas report\n\n| Module | Target | Status | Confidence |\n|---|---|---|---|\n'+'\n'.join(f"| {r['module']} | {r['target']} | **{r['status']}** | {r['confidence']} |" for r in rows)+'\n',encoding='utf-8')
 elif fmt=='html':p.write_text("<!doctype html><meta charset='utf-8'><title>Recon Atlas</title><h1>Recon Atlas report</h1><table><tr><th>Module</th><th>Target</th><th>Status</th><th>Confidence</th></tr>"+''.join(f"<tr><td>{html.escape(r['module'])}</td><td>{html.escape(r['target'])}</td><td>{html.escape(r['status'])}</td><td>{html.escape(r['confidence'])}</td></tr>" for r in rows)+'</table>',encoding='utf-8')
 else:raise ValueError('unsupported format')
