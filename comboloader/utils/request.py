import httplib2
import json
from webob import Response
import logging
import pprint
import os.path


log = logging.getLogger(__name__)
pp = pprint.PrettyPrinter()

class RequestLoader(object):
    """ComboLoader Object
    
    Creates a combo loader object 
    """
    def __call__(self, *args, **kwargs):
        return self.combine()

    def combine(self):
        return ""
        
class HttpRequest(RequestLoader):
    pass

class FileRequest(RequestLoader):
    """FileRequest loads files with a base and path
    
    Concatenates the files given in a list
    
    """
    def __init__(self, request, base, files):
        self.files = files
        self.base = base
        self.request = request
                
    def combine(self):
        content = ""
 
        for file in self.files:
            path = os.path.abspath(os.path.join(self.base, file))
            log.debug("File Type: %s :::: File Path: %s" % (file_type, path))
            try:
                f = open(path, 'r')
                content += f.read()
                f.close()
            except IOError as e:
                log.error("File not found: %s ::: Continuing..." % e)
        
        return content
