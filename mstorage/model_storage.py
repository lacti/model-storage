# -*- coding: utf-8 -*-
import os
import json
import uuid
import hashlib

import fire
import boto3

from .logger import Logger
from .database import Database


class ModelStorage(object):
    def __init__(self):
        self.__logger = Logger(prefix='ModelStorage')
        self.__s3 = boto3.resource('s3')

        apath = os.path.abspath(os.path.dirname(__file__))
        tpath = os.path.join(apath, './config/mstorage.json')
        self.__config = json.load(open(tpath))
        self.__bucket = self.__config['s3']['bucket']
        self.__db = Database(self.__config['db_connection'])

    def __generate_version(self):
        v = uuid.uuid4()
        return str(v)

    def __get_checksum(self, path, blocksize=2**20):
        m = hashlib.md5()
        with open(path, "rb") as f:
            while True:
                buf = f.read(blocksize)
                if not buf:
                    break
                m.update(buf)
        return m.hexdigest()

    def push(self, service, model, local_fname, active=True):
        assert os.path.isfile(local_fname), 'must be file: [%s]' % src_model_fname

        v = self.__generate_version()
        s3_key = '%s/%s/%s' % (service, model, v)
        self.__s3.meta.client.upload_file(local_fname, self.__bucket, s3_key)

        checksum = self.__get_checksum(local_fname)
        self.__db.insert(service=service,
                         model=model,
                         version=v,
                         s3_key=s3_key,
                         local_fname=local_fname,
                         checksum=checksum,
                         active=active)
        self.__logger.info('model pushed successfully')

    def pull(self, service, model, out_fname, version=None):
        meta = self.__db.get(service, model, version=version)
        s3_key = meta['s3_key']
        self.__s3.meta.client.download_file(self.__bucket,
                                            s3_key,
                                            out_fname)
        check = self.__get_checksum(out_fname)
        assert meta['checksum'] == check, 'checksum is broken, origin[%s]:local[%s]' % (meta['checksum'], check)
        self.__logger.info('download finished')

    def list(self, service, model, limit=10):
        versions = self.__db.list(service, model)
        for v in versions:
            self.__logger.info('version: [%s], created: [%s], s3_key: [%s], machine_name: [%s]',
                               v['version'],
                               v['create_ts'],
                               v['s3_key'],
                               v['machine_name'],
                               )

    def create_table(self):
        from .table import create_table
        create_table(self.__config['db_connection'], self.__logger)


def cli():
    fire.Fire(ModelStorage)
