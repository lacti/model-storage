# -*- coding: utf-8 -*-
import os
import json
import uuid

import fire
import boto3

from .logger import Logger
from .database import Database


class ModelStorage(object):
    def __init__(self, bucket_name):
        self.__logger = Logger(prefix='ModelStorage')
        self.__s3 = boto3.resource('s3')
        self.__config = json.load(open('./config/mstorage.json'))
        self.__bucket_name = self.__config['s3']['bucket']
        self.__db = Database(self.__config['db_connection'])

    def push(self, service, model_name, src_fname, **kwargs):
        assert os.path.isfile(src_fname), 'must be file: [%s]' % src_model_fname

        v = self.__db.generate_version(service, model_name)
        s3_key = '%s/%s/%s' % (service, model_name, v)
        self.__s3.meta.client.upload_file(src_fname, 'pubg-model-storage', s3_key)
        self.__db.commit_version(service, model_name, s3_key, kwargs)

    def pull(self, service, model_name, out_fname):
        meta = self.__db.get_lastest(service, model_name)
        s3_key = meta['s3_key']
        self.__s3.download_file(self.__bucket_name,
                                s3_key,
                                out_fname)


def cli():
    fire.Fire(ModelStorage)
