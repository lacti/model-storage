# -*- coding: utf-8 -*-
import json
import uuid

import fire
import boto3

from .logger import Logger


class ModelStorage(object):
    def __init__(self):
        self.logger = Logger(prefix='ModelStorage')
        self.s3 = boto3.resource('s3')

    def push(self, service, model_name, src_fname, bucket_name, **kwargs):
        assert self.__validate_bucket(bucket_name), 'TODO'
        assert self.__validate_push(service, src_fname, model_fname), 'TODO'
        s3_path = '%s/%s/%s' % (service, model_name, version)
        s3.meta.client.upload_file(src_fname, s3_path)
        raise NotImplementedError

    def pull(self, bucket_name, service, model_name, out_fname, **kwargs):
        assert self.__validate_bucket(bucket_name), 'TODO'
        assert self.__validate_pull(service, out_name, model_fname)
        raise NotImplementedError

    def __mkdir_s3(self, path):
        return False

    def __validate_bucket(self, bucket):
        raise NotImplementedError
        return False

    def __validate(self, service, model_name):
        raise NotImplementedError
        return False

    def __validate_push(self, service, model_name, src_model_fname):
        assert self.__validate(service, model_name), 'TODO'
        raise NotImplementedError

    def __validate_pull(self, service, model_name, out_model_fname):
        assert self.__validate(service, model_name), 'TODO'
        raise NotImplementedError


def cli():
    ms = ModelStorage()
    fire.Fire(ms)
