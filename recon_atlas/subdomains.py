from pathlib import Path
from .dns import candidates
def from_wordlist(s,path,mode="passive"): return candidates(s,Path(path).read_text(encoding="utf-8").splitlines(),mode)
