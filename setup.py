#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
#from distutils.core import setup
from setuptools import setup

README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name = 'django-tribe-client',
    version = '0.0.1',
    author = 'Rene A. Zelaya',
    author_email = 'Rene.Armando.Zelaya.Favila@dartmouth.edu',
    packages = ['tribe-client'],
    include_package_data = True,
    url = 'https://bitbucket.org/greenelab/tribe-client',
    license = 'LICENSE.txt',
    description = 'Reusable Django app to connect servers with the Tribe web service at Dartmouth College',
    long_description = open('README.rst').read(),
    install_requires = [
        'requests == 2.1.0',
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
    ],
)
