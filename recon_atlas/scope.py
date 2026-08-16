import ipaddress
from datetime import datetime,timezone
from urllib.parse import urlparse
from .models import Scope
class ScopeViolation(ValueError): pass
def _dt(v): return datetime.fromisoformat(v.replace('Z','+00:00'))
def validate_scope(s):
 e=[]
 if not s.scope_id:e.append('scope_id is required')
 if not s.operator:e.append('operator is required')
 if not s.authorized_by:e.append('authorized_by is required')
 if not (s.domains or s.hosts or s.cidrs):e.append('at least one target is required')
 if _dt(s.valid_until)<=_dt(s.valid_from):e.append('valid_until must be after valid_from')
 if s.max_requests<=0 or s.max_connections<=0:e.append('budgets must be positive')
 if not 1<=s.max_concurrency<=32:e.append('max_concurrency must be between 1 and 32')
 if s.min_delay_ms<0:e.append('min_delay_ms cannot be negative')
 if any(p<1 or p>65535 for p in s.ports):e.append('invalid port')
 if any(not x.startswith('/') for x in s.path_prefixes):e.append('path prefix must start with /')
 return e
def require_target(s,target):
 h=(urlparse(target).hostname or '') if '://' in target else target; h=h.lower().rstrip('.')
 allowed=any(h==d.lower().lstrip('*.') or h.endswith('.'+d.lower().lstrip('*.')) for d in s.domains) or h in {x.lower() for x in s.hosts}
 try:
  ip=ipaddress.ip_address(h); allowed=allowed or any(ip in ipaddress.ip_network(n,strict=False) for n in s.cidrs)
  if ip.is_private and not s.allow_private: raise ScopeViolation('private target blocked by scope')
 except ValueError: pass
 if not allowed: raise ScopeViolation('target outside authorized scope: '+h)
 return h
def require_port(s,p):
 if p not in s.ports: raise ScopeViolation('port outside authorized scope: '+str(p))
def require_path(s,path):
 if not any(path.startswith(x) for x in s.path_prefixes): raise ScopeViolation('path outside authorized prefixes: '+path)
def enforce_window(s,now=None):
 n=now or datetime.now(timezone.utc)
 if not (_dt(s.valid_from)<=n<=_dt(s.valid_until)): raise ScopeViolation('execution outside authorization window')
