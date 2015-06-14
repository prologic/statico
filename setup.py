#!/usr/bin/env python


import re
from setuptools import setup


version = re.search(
    '^__version__\s*=\s*"(.*)"',
    open('statico/statico.py').read(),
    re.M
    ).group(1)

setup(name='statico',
      version=version,
      description='Static site generator',
      long_description=open('README.me').read(),
      author='Ossama Edbali',
      author_email='ossedb@gmail.com',
      url='https://github.com/oss6/statico/',
      license='MIT',
      include_package_data=True,
      platforms='any',
      packages=['statico'],
      entry_points={
        "console_scripts": ['statico = statico.statico:main']
      },
)