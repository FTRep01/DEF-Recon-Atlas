import threading,time
class Budget:
 def __init__(self,requests,connections,delay): self.requests=requests; self.connections=connections; self.delay=delay/1000; self.lock=threading.Lock(); self.last=0
 def request(self):
  with self.lock:
   if self.requests<=0: raise RuntimeError('request budget exhausted')
   wait=self.delay-(time.monotonic()-self.last)
   if wait>0: time.sleep(wait)
   self.requests-=1; self.last=time.monotonic()
 def connection(self):
  with self.lock:
   if self.connections<=0: raise RuntimeError('connection budget exhausted')
   self.connections-=1
