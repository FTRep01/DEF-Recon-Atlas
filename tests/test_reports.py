import tempfile,unittest
from pathlib import Path
from recon_atlas.reports import write_report
class T(unittest.TestCase):
 def test_reports(self):
  r={'findings':[{'finding_id':'x','module':'dns','target':'example.com','status':'resolved','confidence':'high','method':'dns','observed_at':'now'}]}
  with tempfile.TemporaryDirectory() as d:
   write_report(r,'json',str(Path(d)/'a.json'));write_report(r,'markdown',str(Path(d)/'a.md'));self.assertIn('example.com',(Path(d)/'a.md').read_text())
