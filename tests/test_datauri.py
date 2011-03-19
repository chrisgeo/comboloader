"""test_datauri.py
Test data_uri class, substituting urls in files, with data uri.

"""
import unittest
from combloader.utils.data_uri import DataURI

class TestDataURI(unittests.TestCase):
  def ssetUp(self):
   self.data_uri = DataURI() 
  
  def test_data_uri_from_local_path(self):
    pass

  def test_data_uri_from_url(self):
    pass
