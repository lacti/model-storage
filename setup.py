# -*- coding: utf-8 -*-
from pip.req import parse_requirements
from setuptools import setup, find_packages
from setuptools.command.install import install


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

with open('requirements.txt') as f:
    required = f.read().splitlines()


class InstallCommand(install):
    user_options = install.user_options + [
        ('config-path=', None, None) # an option that takes a value
    ]

    def initialize_options(self):
        install.initialize_options(self)
        self.config_path = None

    def finalize_options(self):
        print("config-path is [%s]" % self.config_path)
        install.finalize_options(self)

    def run(self):
        global config_path
        config_path = self.config_path
        if config_path is None:
            assert False, 'no config-path, stop installer'

        # validate config file
        import os
        assert os.path.isfile(config_path), 'given parameter is not a file [%s]' % config_path

        import json
        content = json.load(open(config_path))
        _ = content['s3']['bucket']
        _ = content['db_connection']['host']
        _ = content['db_connection']['user']
        _ = content['db_connection']['password']
        _ = content['db_connection']['database']

        # copy config file
        import shutil
        apath = os.path.abspath(os.path.dirname(__file__))
        tpath = os.path.join(apath, './mstorage/config/mstorage.json')
        shutil.copy(config_path, tpath)

        install.run(self)


setup(
    name='mstorage',
    version='0.0.1',
    description='Model Storage based on AWS S3 and MySQL',
    long_description=readme,
    author='Hyunjong Lee',
    author_email='https://github.com/hyunjong-lee/model-storage/wiki',
    url='https://github.com/hyunjong-lee/model-storage',
    license=license,
    install_requires=required,
    cmdclass={
        'install': InstallCommand,
    },
    packages=find_packages(exclude=('tests', 'docs')),
    entry_points={
        'console_scripts': ['mstorage=mstorage.model_storage:cli'],
    },
)

