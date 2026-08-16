import unittest
from recon_atlas.models import Scope
from recon_atlas.scope import validate_scope,ScopeViolation,require_target,require_port
class T(unittest.TestCase):
 def setUp(self):self.s=Scope('x','op','owner','2020-01-01T00:00:00Z','2099-01-01T00:00:00Z',domains=['example.com'],ports=[443])
 def test_valid(self):self.assertEqual(validate_scope(self.s),[])
 def test_target(self):
  with self.assertRaises(ScopeViolation):require_target(self.s,'other.com')
 def test_port(self):
  with self.assertRaises(ScopeViolation):require_port(self.s,22)
