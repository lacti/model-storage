# -*- coding: utf-8 -*-
from logzero import logger


class Logger:
    def __init__(self, prefix=None):
        self.prefix = prefix

    def __print(self, printer, msg, *args):
        f_msg = msg % args
        if self.prefix:
            f_msg = '[%s] %s' % (self.prefix, f_msg)
        printer(f_msg)

    def info(self, msg, *args):
        self.__print(logger.info, msg, *args)

    def debug(self, msg, *args):
        self.__print(logger.debug, msg, *args)

    def warn(self, msg, *args):
        self.__print(logger.debug, msg, *args)

    def error(self, msg, *args):
        self.__print(logger.debug, msg, *args)
