"""test_datauri.py
Test data_uri class, substituting urls in files, with data uri.

"""
import unittest
import os
from comboloader.utils.data_uri import DataURI
from nose.tools import raises

test_file = './tmp.txt'

class TestDataURI(unittest.TestCase):
  def setUp(self):
    self.data_uri = DataURI() 
    file = open(test_file, 'w')
    file.write('Testing some content')
    file.close()
  
  def tearDown(self):
    os.remove(test_file)

  def test_data_uri_from_local_path(self):
    expected = \
      'data:text/plain;charset=utf-8;base64,VGVzdGluZyBzb21lIGNvbnRlbnQ='
    result = self.data_uri.encode(test_file)
    assert result == expected

  def test_data_uri_from_url(self):
    pass

  @raises(Exception)
  def test_data_uri_file_not_exist(self):
    self.data_uri.encode('somefile.png')
