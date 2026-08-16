import socket
from concurrent.futures import ThreadPoolExecutor,as_completed
from .budget import Budget
from .evidence import make_finding
from .scope import require_target,require_port
def scan(s,host):
 require_target(s,host); b=Budget(s.max_requests,s.max_connections,s.min_delay_ms)
 def one(p):
  require_port(s,p); b.connection()
  try:
   b.request(); x=socket.create_connection((host,p),timeout=2); x.close(); return make_finding('ports',f'{host}:{p}','open','high',{'port':p,'transport':'tcp'},'tcp-connect','No protocol payload was sent.')
  except (OSError,RuntimeError) as e:return make_finding('ports',f'{host}:{p}','closed_or_filtered','medium',{'port':p,'error':type(e).__name__},'tcp-connect')
 with ThreadPoolExecutor(max_workers=s.max_concurrency) as pool:return [x.result() for x in as_completed([pool.submit(one,p) for p in s.ports])]
