#!/usr/bin/env python
import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

VERSION = '0.0.1'

if sys.argv[-1] == 'clean':
    os.system('rm -rf *.egg-info')
    os.system('rm -rf build')
    os.system('rm -rf dist')
    sys.exit()

setup(
    name = 'jem',
    author = 'jkal',
    author_email = 'john@jkal.net',
    url = 'http://github.com/jkal/jem',
    version = VERSION,
    packages = [
        'jem',
        'jem.commands'
    ],
    scripts  = [
        'bin/jem'
    ],
    install_requires = [
        'peewee==2.3.1',
        'click==3.2',
        'xattr==0.7.5',
        'biplist==0.8'
    ],
    zip_safe = False,
    description = 'jem',
    long_description = 'jem'
)