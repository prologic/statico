#!/usr/bin/env python


from setuptools import setup
import statico.statico as st

setup(name='statico',
      version=st.__version__,
      description='Static site generator',
      long_description=open('README.rst').read(),
      author='Ossama Edbali',
      author_email='ossedb@gmail.com',
      url='https://github.com/oss6/statico/',
      license='MIT',
      platforms='any',
      classifiers=[
          'Intended Audience :: Developers',
          'Intended Audience :: Information Technology',
          'License :: OSI Approved :: MIT License',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 3.4',
          'Topic :: Utilities'
      ],
      packages=['statico'],
      include_package_data=True,
      install_requires=[
          'Markdown==2.6.2',
          'Jinja2==2.7.3',
          'github3.py==0.9.4'
      ],
      entry_points={
        "console_scripts": ['statico = statico.statico:run']
      },
)