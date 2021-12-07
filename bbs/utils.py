"""
# coding:utf-8
@Time    : 2021/12/06
@Author  : jiangwei
@File    : utils.py
@Desc    : utils
@email   : qq804022023@gmail.com
@Software: PyCharm
"""
import logging
from logging.handlers import RotatingFileHandler
from bbs.setting import basedir
import os
import datetime


def singleton(cls):
    instances = {}

    def inner(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
            return instances[cls]

    return inner


@singleton
class LogUtil:
    def __init__(self, log_name, log_path, max_size=2 * 1024 * 1024, backup_count=10):
        self.logger = self.log_util(log_name, log_path, max_size, backup_count)

    @staticmethod
    def log_util(log_name, log_path, max_size=2 * 1024 * 1024, backup_count=10):
        if not os.path.exists(log_path):
            os.mkdir(log_path)
        logger = logging.getLogger(log_name)
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        file_handler = RotatingFileHandler(log_path + '/' + log_name,
                                           maxBytes=max_size,
                                           backupCount=backup_count
                                           )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        logger.setLevel(logging.DEBUG)
        return logger
