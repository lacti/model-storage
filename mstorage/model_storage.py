# -*- coding: utf-8 -*-
import json
import fire

from .logger import Logger


class ModelStorage(object):
    def __init__(self, config_fname):
        self.config = json.load(open(config_fname).read())
        self.logger = Logger(prefix='ModelStorage')

    def push(self, service, model_name, src_fname, **kwargs):
        assert __validate_push(service, src_fname, model_fname)
        raise NotImplementedError

    def pull(self, service, model_name, out_fname, **kwargs):
        assert __validate_pull(service, out_name, model_fname)
        raise NotImplementedError

    def __validate(self, service, model_name):
        raise NotImplementedError

    def __validate_push(self, service, model_name, src_model_fname):
        assert __validate(service, model_name), 'TODO'
        raise NotImplementedError

    def __validate_pull(self, service, model_name, out_model_fname):
        assert __validate(service, model_name), 'TODO'
        raise NotImplementedError
