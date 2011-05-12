import unittest
from mock import Mock
from comboloader.app import ComboLoaderApp

config = {
      'base': './build/',
      'separator': ';'
    }
environ = {}

def TestComboLoader(unittest.UnitTest):
  def setUp(self):
    self.app = Mock()
    self.cm = ComboLoaderApp(self.app)
    #set up some fake files with content

  def tearDown(self):
    #remove files

  def test_app(self):
    pass
