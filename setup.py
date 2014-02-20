#!/usr/bin/env python

from distutils.core import setup

setup(name='wattindicator',
      version='1.2',
      description='Simple power monitor indicator for Ubuntu',
      author='Leonardo Robol',
      author_email='leo@robol.it',
      url='http://github.com/robol/wattindicator',
      scripts = [ 'wattindicator' ],
      data_files = [ 
          ('share/wattindicator', [ 'lightning.png' ],), 
          ('share/man/man1', [ 'wattindicator.1' ] ,)
      ]
     )
