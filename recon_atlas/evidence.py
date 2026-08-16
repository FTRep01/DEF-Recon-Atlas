import hashlib
from .models import Finding,now_iso
def make_finding(module,target,status,confidence,evidence,method,notes=''):
 fid=hashlib.sha1((module+'|'+target).encode()).hexdigest()[:16]
 return Finding(module+'-'+fid,module,target,status,confidence,now_iso(),evidence,method,notes)
