# -*- coding: utf-8 -*-
from pip.req import parse_requirements
from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='model-storage',
    version='0.0.1',
    description='Model Storage based on AWS S3 and MySQL',
    long_description=readme,
    author='Hyunjong Lee',
    author_email='https://github.com/hyunjong-lee/model-storage/wiki',
    url='https://github.com/hyunjong-lee/model-storage',
    license=license,
    install_requires=required,
    packages=find_packages(exclude=('tests', 'docs')),
    entry_points={
        'console_scripts': ['mstorage=mstorage.ModelStorage:cli'],
    },
)

