from dataclasses import dataclass,asdict,field
from datetime import datetime,timezone
from typing import Any
def now_iso(): return datetime.now(timezone.utc).isoformat()
@dataclass
class Scope:
 scope_id:str; operator:str; authorized_by:str; valid_from:str; valid_until:str; domains:list[str]=field(default_factory=list); hosts:list[str]=field(default_factory=list); cidrs:list[str]=field(default_factory=list); ports:list[int]=field(default_factory=list); path_prefixes:list[str]=field(default_factory=lambda:['/']); max_requests:int=100; max_connections:int=50; min_delay_ms:int=250; max_concurrency:int=4; allow_private:bool=False; contact:str=''; user_agent:str='ReconAtlas/0.1'
@dataclass
class Finding:
 finding_id:str; module:str; target:str; status:str; confidence:str; observed_at:str; evidence:dict[str,Any]; method:str; notes:str=''
 def to_dict(self): return asdict(self)
@dataclass
class Run:
 run_id:str; started_at:str; scope_id:str; scope_sha256:str; modules:list[str]; findings:list[dict[str,Any]]; stats:dict[str,Any]; errors:list[str]
 def to_dict(self): return asdict(self)
