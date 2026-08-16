import unittest
from recon_atlas.http_paths import title
class T(unittest.TestCase):
 def test_title(self):self.assertEqual(title('<title> Hello   Atlas </title>'),'Hello Atlas')
