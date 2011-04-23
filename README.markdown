ComboLoader
-----------
WSGI based app that takes a request and concatenates the given files into a single file, and returns it as a single request.

REQUIREMENTS
---------------
  * Paste>=1.7
  * PasteScript>=1.7
  * WebOb>=0.9.8
  * httplib2>=0.50
  * python-magic>=0.4

WHAT CAN IT DO?
---------------
  * Replace url() tags with:
    - data uris

WHAT I WANT IT TO DO/IDEA MAPPING
---------------------------------
  * Ability to use a dependency graph for a file
  * automatically replace url() with either:
      - provided base url for a CDN, etc
  * Lazy Loading
    - Request knowledge - if a page/referrer asks for a URL cache it and/or keep track of the files loaded so not to load for that page again
      :: how long? to wait, seconds? Milliseconds?
      :: Definitely cache the page/request string
    - Preloader?
  * Track most used files, create a combined/combo/rollup?
    - Log files used so we can put some analytics
    - Log requests and urls + referrers

For any other requests please submit a bug in github. https://github.com/chrisgeo/comboloader/issues

# Example config
```ini
    
    [server:main]
    use = egg:Paste#http
    host = 0.0.0.0
    port = 80
    
    [composite:main]
    use = egg:Paste#urlmap
    / = YOURAPP
    /combo  = loader
    
    [app:loader]
    use = egg:comboloader
    use_config = False

    [app:YOURAPP]
    use = egg:YOURAPP
    full_stack = true
```

COMMON ISSUES
--------------

python-magic
  This is required for automatically finding the mime-type of a file without depending on extensions, etc. As such, it requires libmagic to be installed. A known issue with python-magic on darwin (OS X) systems is that it depends on MacPorts. This will hopefully be fixed soon.

