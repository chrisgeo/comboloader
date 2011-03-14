"""
  Data URI
    Process data uris for insertion into CSS files on the fly, possibly even
    provide a utility for WSGI Apps

    Format:
    data:[<MIME-type>][;charset=<encoding>][;base64],<data>

"""
from base64 import b64encode

class DataURI(object):
  template = 'data:{mime};charset={encoding};base64,{data}'

  def _get_and_encode_content(self, file):
    fopen = open(file, 'r')
    contents = fopen.read() #entire file contacts
    fopen.close()

    #encode contents in base64
    return b64encode(contents)


  def encode(self, file):
    """ Encodes file and returns data uri
    """
    encoded_content = self._get_and_encode_content(file)
    if not encoded_content:
      raise Exception("No content in file::%s", file)
    #figure out type of file from extention, python-magic

