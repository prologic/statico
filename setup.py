#!/usr/bin/env python


import re
from setuptools import setup


version = re.search(
    '^__version__\s*=\s*"(.*)"',
    open('statico/statico.py').read(),
    re.M
    ).group(1)


with open('README.me', 'rb') as f:
    long_description = f.read().decode("utf-8")


"""def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)

long_description = read('README.md',)"""

setup(name='statico',
      version=version,
      description='Static site generator',
      long_description=long_description,
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