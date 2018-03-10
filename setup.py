# -*- coding: utf-8 -*-
from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='model-storage',
    version='0.1.0',
    description='Model Storage based on AWS S3 and MySQL',
    long_description=readme,
    author='Hyunjong Lee',
    author_email='https://github.com/hyunjong-lee/model-storage/wiki',
    url='https://github.com/kennethreitz/samplemod',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)

