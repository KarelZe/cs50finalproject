# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='sample',
    version='0.0.1',
    description='sample',
    long_description=readme,
    author='Markus Bilz',
    author_email='mail@markusbilz.com',
    url='www.markusbilz.com',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)

