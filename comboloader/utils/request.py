import httplib2
import json


class HttpRequest(object);
    
    def __init__(self, base, path):
        pass


class FileRequest(object):
    """FileRequest loads files with a base and path
    
    Concatenates the files given in a list
    
    """
    def __init__(self, base, path, file_list):
        self.file_path = base + path
        self.files = file_list
        
    def _combine(self):
        content = ""
        for k in self.files:
            f = open("%s/%s" % (self.file_path, k))
            content += f.read()
            f.close()