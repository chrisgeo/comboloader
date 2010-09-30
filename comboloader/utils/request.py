import httplib2
import json
from webob import Response
import logging
import pprint


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
    def __init__(self, request, config, files):
        self.files = files
        self.config = config
        self.request = request
                
    def combine(self):
        content = ""
 
        for ft, items in self.files.iteritems():
            for item in items:
                try:
                    log.debug("File Type: %s :::: File Path: %s" % (ft, item))
                    f = open("%s/%s" % (self._get_file_path(ft), item), 'r')
                    content += f.read()
                    f.close()
                except IOError as e:
                    log.error("File not found: %s ::: Continuing..." % e)
        
        return content

    def _get_file_path(self, file_type):
        if file_type.lower() == 'js':
            return self.config['js_path']
        elif file_type.lower() == 'css':
            return self.config['css_path']
