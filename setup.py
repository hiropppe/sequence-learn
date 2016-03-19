#!/usr/bin/env python

import os
from setuptools import setup
from srl import __version__

requires = [
]

def read(name):
    return open(os.path.join(os.path.dirname(__file__), name)).read()

setup(
  name='seq-learn',
  version=__version__,
  description='Some utility for sequencial labeling',
  author='take',
  url='',
  packages=[
  ],
  scripts=[
    'scripts/tagging',
  ],
  install_requires=requires,
  license='MIT',
  test_suite='test',
  classifiers = [
    'Operating System :: OS Independent',
    'Environment :: Console',
    'Programming Language :: Python',
    'License :: OSI Approved :: MIT License',
    'Development Status :: 2 - Pre-Alpha',
    'Intended Audience :: Information Technology',
    'Intended Audience :: Science/Research',
    'Topic :: Utilities',
  ],
  data_files = [
  ]
)
