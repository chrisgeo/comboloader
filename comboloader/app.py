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

required_config_keys = ('base')

def parse_yaml_config(config_file):
  """
    Parse YAML file for configuration options 
  """
  pass

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
    new_config['filter'] = config.get('filter', 'min')
    new_config['separator'] = config.get('separator', '&')
    new_config['base_path'] = config['base_path']
    return new_config
    

def parse_config_file(config):

    if asbool(config['use_config']):
        new_config = parse_json_file(config['config_file'])
    else:
        new_config = parse_ini_config(config)
         
    return new_config


class ComboLoaderApp(object):
    """ComboLoader WSGI App
        
        Retrieves files from a filesystem or HTTP Request and concatenates them
        into one file request

    """
    def __init__(self, config):
        self.config = parse_config_file(config)
    
    def __call__(self, environ, start_response):
        req = webob.Request(environ)
        
        if not req.query_string:
            return exc.HTTPBadRequest("Cannot have empty parameter list")(environ, start_response)

        separator = self.config['separator']
        content_type = 'text/plain' #default content-type

        files = req.query_string.split(separator)
        if files:
            if files[0].endswith('.js')
               content_type = 'text/javascript'
            elif files[0].endswith('.css'):
                content_type = 'text/css'

            resp = self.config['request_type'](request=req,
                    config=self.config, files=files)

            return Response(status=200, 
                            body=resp.combine(), 
                            content_type=content_type,
                            )(environ, start_response)
        else:
            return exc.HTTPBadRequest("404 Not Found")(environ, start_response)

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
