#!/usr/bin/env python
from __future__ import unicode_literals
from setuptools import setup, find_packages

install_requires = [
    "MySQL-python==1.2.5",
    "psycopg2==2.6.1",
    "nevow==0.13.0",
    "pillow>=3.1.1",
    "twisted>=12.3.0",
]

setup(
    name='pyicqt',
    version='8.1.6',
    description='ICQ Transport for Jabber, implemented with Python'
                ' and Twisted',
    author='Michael Franke',
    author_email='mf33456@gmail.com',
    url='https://github.com/2mf/pyicqt',
    entry_points={
        'console_scripts': [
            'pyicqt = pyicqt.main:main',
        ],
    },
    packages=find_packages(exclude=("tests", "tests.*")),
    install_requires=install_requires,
    include_package_data=True,
    license="GNU GPL v2",
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: Apache Software License",
        "Topic :: Software Development :: Testing",
    ],
)
