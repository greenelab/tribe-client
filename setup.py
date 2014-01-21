#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
try:
    from distutils.core import setup
except ImportError:
    from setuptools import setup

README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name = 'tribe-client',
    version = '0.1.0',
    author = 'Rene A. Zelaya',
    author_email = 'Rene.Armando.Zelaya.Favila@dartmouth.edu',
    packages = [],
    scripts = [],
    url = '',
    license = 'LICENSE.txt',
    description = 'App to connect with the Tribe web service',
    long_description = open('README.txt').read(),
    install_requires = [
        "Django >= 1.6.0",
        "requests == 2.1.0",
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License', # example license
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
    ],
)
