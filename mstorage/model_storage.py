# -*- coding: utf-8 -*-
import json
import uuid

import fire
import boto3

from .logger import Logger


class ModelStorage(object):
    def __init__(self, bucket_name):
        self.logger = Logger(prefix='ModelStorage')
        self.__validate_bucket(bucket_name)
        self.bucket_name = bucket_name
        self.s3 = boto3.resource('s3')

    def push(self, service, model_name, src_fname, **kwargs):
        assert __validate_push(service, src_fname, model_fname)
        s3_path = '%s/%s/%s' % (service, model_name, version)
        s3.meta.client.upload_file(src_fname, self.bucket_name, s3_path)
        raise NotImplementedError

    def pull(self, service, model_name, out_fname, **kwargs):
        assert __validate_pull(service, out_name, model_fname)
        raise NotImplementedError

    def mkdir(self, path):
        pass

    def __validate_bucket(self, bucket):

        pass

    def __validate(self, service, model_name):
        raise NotImplementedError

    def __validate_push(self, service, model_name, src_model_fname):
        assert __validate(service, model_name), 'TODO'
        raise NotImplementedError

    def __validate_pull(self, service, model_name, out_model_fname):
        assert __validate(service, model_name), 'TODO'
        raise NotImplementedError

