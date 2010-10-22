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
from comboloader.utils import HttpRequest, FileRequest
from beaker.middleware import SessionMiddleware
from paste.deploy.converters import asbool
from webob import Response
import logging

log = logging.getLogger(__name__)

REQUEST_TYPES = {
    'server': HttpRequest,
    'file': FileRequest
}

required_config_keys = ('base', 'request_type', 'js_path', 'css_path', 'combo_base')


def parse_json_confing(config_file):
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
    
    Otherwise uses the *.ini file to load the server config

    """ 
    f = open(config_file, 'r')
    content = f.read()
    f.close()
    
    config = json.loads(content)
    
    
    #parse through options to load files by file name
    missing_keys = []
    for key in required_config_keys:
        if key not in config:
            missing_keys.append(key)
    if missing_keys:
        raise Exception("Required keys are missing in config :: required are: %s ::: config is missing: %s" 
                        % (required_config_keys, missing_keys))
    
    config['request_type'] = REQUEST_TYPES[config['request_type'].lower()]
    
    return config


def parse_ini_config(config):
    
    new_config = {}
    
    new_config['request_type'] = REQUEST_TYPES['file']
    new_config['js_path'] = config['base_js_dir']
    new_config['css_path'] = config['base_css_dir']
    new_config['img_path'] = config['base_img_dir']
    new_config['filter'] = config.get('filter', 'min')
    
    return new_config
    

def parse_config_file(config):

    if asbool(config['use_config']):
        new_config = parse_json_file(config['config_file'])
    else:
        new_config = parse_ini_config(config)
         
    return new_config


def get_content_type(files):
    if 'js' in files and files.get('js') is not None:
        return 'application/javascript'
    elif 'css' in files and files.get('css') is not None:
        return 'text/css'


class ComboLoaderApp(object):
    """ComboLoader WSGI App
        
        Retrieves files from a filesystem or HTTP Request and concatenates them
        into one file request

    """
    def __init__(self, config):
        self.config = parse_config_file(config)
        
    def __call__(self, environ, start_response):
        req = webob.Request(environ)
        req.session = environ['beaker.session']
        
        #get files and munge together
        #command line arguments
        if not req.query_string:
            return exc.HTTPBadRequest("Cannot have empty parameter list")(environ, start_response)

        files = {}

        for param in req.query_string.split('&'):
            log.debug("param is %s", param)
            if param.endswith('.js'):
                if not files.get('js') and not isinstance(files.get('js'), list):  
                    files['js'] = list()
                files['js'].append(param)
            elif param.endswith('.css'):
                if not files.get('css') and not isinstance(files.get('css'), list):  
                    files['css'] = list()
                files['css'].append(param)
        
        resp = self.config['request_type'](request=req, config=self.config, files=files)

        return Response(status=200, 
                        body=resp.combine(), 
                        content_type=get_content_type(files),
                        )(environ, start_response)


def make_app(config):
        """Construct WSGI App from JSON file"""
        app = ComboLoaderApp(config)
        app = SessionMiddleware(app, config)
        return app
         

def make_loader_app(global_conf, **app_conf):
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
        base_js_dir = %(here)s/js/
        base_css_dir = %(here)s/css/
        use_config = False
        [app:YOURAPP]
        use = egg:YOURAPP
        full_stack = true
        static_files = true

    """
    app = ComboLoaderApp(app_conf)
    app = SessionMiddleware(app, app_conf)  
    return app
