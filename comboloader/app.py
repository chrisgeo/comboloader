"""Combo Loader WSGI App

Variable location combo loader to import javascript and css files.

It will loader Javascript files into one JS and CSS into another much like YUI PHP Loader: 
http://developer.yahoo.com/yui/phploader/

TODO:
Build in caching beaker, sessions, and/or memcache.

"""

import sys
import webob
import webob.exc as exc
import json

from beaker.middleware import SessionMiddleware

REQUEST_TYPES = {
    'server': utils.HttpRequest,
    'file': utils.FileRequest
}

required_config_keys = ['base', 'request_type', 'js_path', 'css_path']

def parse_config_file(config_file):
    """Parse JSON for config 
    
    JSON will can look like this:
    
    {
        "request_type": "server",
        "comboBase": "www.cdn.com"
        "base": "/base/path", //build directory
        "js_path": "js", //path relative to base
        "css_path": "path/to/css", //path relative to base; note: combo loader will try and search/replace images in CSS files
        "filter": DEBUG|MIN
    }
    
    """
    f = open(config_file, 'r')
    content = f.read()
    f.close()
    config = json.loads(content)
    
    
    #parse through options to load files by file name
    if not required_config_keys in config.keys():
        raise Exception("Required keys are missing in config :: required are: %s ::: config has: %s" 
                                % (required_keys, config.keys()))
    
    config['request_type'] = REQUEST_TYPES[config['request_type'].lower()]
            
    return config

class ComboLoader(object):
    """ComboLoader Object
    
    Creates a combo loader object 
    """
    
    def __init__(self, config_file):
        self.config = parse_config_file(config_file)
        
    def __call__(self, request):
        pass
        
class ComboLoaderApp(object):

    def __init__(self, config_file):
        self.config = json.loads(config)
    
    def __call__(self, environ, start_response):
        req = webob.Request(environ)
        req.session = environ['beaker.session']
        
        schema = req.scheme #get schema for base url to support https if we must
        #get files and munge together
        #command line arguments
        params = dict([part.split('=') for part in req.query_string.split('&')])
        
        
    
def make_app(global_conf, config_file, **app_conf):
    """Construct a complete WSGI app ready to serve by Paste
    
    Example INI file:
    
    .. code-block:: ini
        
        [server:main]
        use = egg:Paste#http
        host = 0.0.0.0
        port = 80

        [composite:main]
        use = egg:Paste#urlmap
        / = YOURAPP
        /loader = loader

        [app:loader]
        use = egg:comboloader
        config_file = %(here)s/LOCATION_TO/CONFIG.json
        beaker.session.data_dir = %(here)s/data/sdata
        beaker.session.lock_dir = %(here)s/data/slock
        beaker.session.key = comboloader
        beaker.session.secret = somesecret
        beaker.session.type = cookie
        beaker.session.validate_key = STRONG_KEY_HERE
        beaker.session.cookie_domain = .yourdomain.com

        [app:YOURAPP]
        use = egg:YOURAPP
        full_stack = true
        static_files = true
    """
    
    app = ComboLoaderApp(config_file)
    app = SessionMiddleware(app, app_conf)
    return app
