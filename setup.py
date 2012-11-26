#!/usr/bin/env python

from setuptools import setup, find_packages

with open('README.rst') as file:
        long_description = file.read()

setup(
    name='openerp_xmlrpc',
    version="0.1",
    author='Grishma Shukla',
    author_email='grs3012@gmail.com',
    description='Xmlrpc Api library for OpenERP',
    long_description=long_description,
    url='https://github.com/Aquasys/openerp_xmlrpc_api',
    include_package_data=True,
    packages=find_packages(),
    classifiers=[
        "Development Status :: 1 - Alpha",
        "License :: OSI Approved :: BSD License",
        "Framework :: OpenERP",
        "Environment :: OpenERP",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python",
    ],
)
