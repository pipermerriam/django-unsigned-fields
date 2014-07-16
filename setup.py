#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

import django_unsigned_fields


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

version = django_unsigned_fields.__version__

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    print("You probably want to also tag the version now:")
    print("  git tag -a %s -m 'version %s'" % (version, version))
    print("  git push --tags")
    sys.exit()

readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='django-unsigned-fields',
    version=version,
    description="""Django fields for using unsigned integers for relationships""",
    long_description=readme + '\n\n' + history,
    author='Piper Merriam',
    author_email='piper@simpleenergy.com',
    url='https://github.com/simpleenergy/django-unsigned-fields',
    packages=[
        'django_unsigned_fields',
    ],
    include_package_data=True,
    install_requires=[
        'django>=1.4',
    ],
    license="BSD",
    zip_safe=False,
    keywords='django-unsigned-fields',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
    ],
)
