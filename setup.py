from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='comboloader',
      version=version,
      description="Combo Loader to load CSS or Javascript files from our any server",
      long_description="""Combo Loader to load CSS or Javascript files from our any server""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author='SurveyMonkey, LLC',
      author_email='chris.george@surveymonkey.com',
      url='http://www.surveymonkey.com',
      license='',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          "WebOb>=0.9.8", "nose>=0.11"
      ],
      entry_points="""
      [paste.app_factory]
      main = comboloader.app:make_loader_app
      """,
      )
