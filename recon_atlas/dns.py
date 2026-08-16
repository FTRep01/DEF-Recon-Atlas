import socket
from .evidence import make_finding
from .scope import require_target
def resolve(s,host):
 require_target(s,host)
 try:
  addrs=sorted({x[4][0] for x in socket.getaddrinfo(host,None,type=socket.SOCK_STREAM)})
  return [make_finding('dns',host,'resolved' if addrs else 'not_found','high' if addrs else 'medium',{'addresses':addrs},'getaddrinfo')]
 except socket.gaierror as e:return [make_finding('dns',host,'not_found','medium',{'error':str(e)},'getaddrinfo')]
def candidates(s,words,mode='passive'):
 out=[]
 for word in words:
  word=word.strip().lower()
  if not word or word.startswith('#'):continue
  for d in s.domains:
   h=word+'.'+d
   out += [make_finding('subdomains',h,'candidate','low',{'source':'operator-wordlist'},'passive-wordlist')] if mode=='passive' else resolve(s,h)
 return out
