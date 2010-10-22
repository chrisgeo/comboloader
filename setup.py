from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='comboloader',
      version=version,
      description="WSGI App for combining JS and CSS files and returning a single request.",
      long_description="WSGI App for combining JS and CSS files and returning a single request.",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='combo, comboloader, combine, javascript, cascading style sheets, css, js',
      author='Chris George',
      author_email='chris.george@surveymonkey.com',
      url='http://www.surveymonkey.com',
      license='GPL',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          "WebOb>=0.9.8", "nose>=0.11", "httplib2>=0.5.0","PasteScript>=1.7","Beaker>=1.5.4","Routes>=1.12.3"
      ],
      entry_points="""
      [paste.app_factory]
      main = comboloader.app:make_loader_app
      """,
      )
