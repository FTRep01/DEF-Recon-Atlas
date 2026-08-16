import hashlib,json
from pathlib import Path
from .models import Scope
def load_scope(path): return Scope(**json.loads(Path(path).read_text(encoding='utf-8')))
def scope_hash(scope): return hashlib.sha256(json.dumps(scope.__dict__,sort_keys=True,separators=(',',':')).encode()).hexdigest()
