from datetime import datetime
import hashlib
import logging

log = logging.getLogger(__name__)

MIME_TYPES = {
    'css' : 'text/css',
    'js'  : 'application/javascript',
    'json': 'application/json',
    'txt' : 'text/plain',
    'xml' : 'application/xml'
    }

#################
#
# Conventience Methods
#
################
def create_hash(string):
  """ Creates an md5 hash to use as a key """
  return hashlib.md5(string).digest() 

def store_cached_value(cached_files, key, content mime_type):
  if key not in cached_files:
    cached_files[key] = {
          'content': content,
          'timestamp': datetime.now(),
          'mimetype': mime_type
        }

def get_mime_type(file):
  parts = file.split('.')
  if len(parts) == 2:
    #get mimetype
    if parts[1] in MIME_TYPES:
      return MIME_TYPES[parts[1]]
    raise UnKnownMimeType("No MIME-TYPE for extention: %s" % parts[1])

  raise Exception("File is unknown")


class UnknownMimeType(Exception):
  def __init__(self, value):
    self.value = value

  def __str__(self):
    return repr(self.value)

