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
from comboloader.utils.common import create_hash, store_cached_value, \
    get_mime_type
from beaker.middleware import SessionMiddleware
from paste.deploy.converters import asbool
from webob import Response
import logging
log = logging.getLogger(__name__)

REQUEST_TYPES = {
    'server': HttpRequest,
    'file': FileRequest
}



REQUIRED_CONFIG_KEYS = ('base')

CACHED_FILES = {} #cache files

#################
#
# Config Parsers
#
#################
def parse_yaml_config(config_file):
  """
    Parse YAML file for configuration options 
  """
  pass


def parse_ini_config(config):
    
    new_config = {}
    
    new_config['request_type'] = REQUEST_TYPES['file']
    new_config['filter'] = config.get('filter', 'min')
    new_config['separator'] = config.get('separator', '&')
    new_config['base_path'] = config['base_path']
    new_config['locale_cache'] = asbool(config.get('locale_cache', 'false'))
    return new_config
    

def parse_config_file(config):

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
        file_hash = None
        
        if not req.query_string:
            return exc.HTTPBadRequest("Cannot have empty parameter list")(environ, start_response)
        
        file_hash = _create_hash(req.query_string)
        mime_type = None
        content = None

        if config['local_cache'] and file_hash in CACHED_FILES:
          mime_type = CACHED_FILES[file_hash]['mime_type']
          content = CACHED_FILES[file_hash]['content']
        else:
          separator = self.config['separator']
          mime_type = 'text/plain' #default content-type

          files = req.query_string.split(separator)
          if files:
              mime_type = get_mime_type(files[0])
              resp = self.config['request_type'](request=req,
                      config=self.config, files=files)
              content = resp.combine()
          else:
              return exc.HTTPBadRequest("404 Not Found")(environ, start_response)

          return Response(status=200, 
                          body=served_files[file_hash]['content'],
                          content_type=files[file_hash]['mimetype'],
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
        base = %(here)s/build/
        separator = ;
        [app:YOURAPP]
        use = egg:YOURAPP
        full_stack = true
        static_files = true

    """
    app = ComboLoaderApp(app_conf)
    app = SessionMiddleware(app, app_conf)
    return app
