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
    def __init__(self, request, config, files):
        self.files = files
        self.config = config
        self.request = request
                
    def combine(self):
        content = ""
 
        for file_type, file_paths in self.files.iteritems():
            for path in file_paths:
                # TODO: Path resolving could benefit memoization
                path = os.path.join(self._get_file_path(file_type), path)
                path = os.path.abspath(path)
                log.debug("File Type: %s :::: File Path: %s" % (file_type, path))
                try:
                    f = open(path, 'r')
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
