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
import yaml
import uuid
import psutil

yaml_file = basedir + '/resources/conf.yaml'
fs = open(yaml_file, encoding='utf8')
conf = yaml.load(fs, Loader=yaml.FullLoader)
config_path = os.path.join(basedir, 'resources/conf.yaml')


class Config(object):
    def __init__(self, path=config_path):
        """
        constructor
        @param path: path of configure file that you need to read or write
        """
        self.path = path
        self.yaml = None
        self.open()
        self.value = None

    def open(self):
        with open(self.path, encoding='utf8') as f:
            self.yaml = yaml.load(f, Loader=yaml.FullLoader)

    def read(self, keys):
        try:
            if isinstance(keys, str):
                return self.yaml.get(keys)
            if isinstance(keys, list):
                for key in keys:
                    self.yaml = self.yaml.get(key)
                value = self.yaml
                self.open()
                return value
            raise Exception('Error key type')
        except Exception as e:
            raise e

    def write(self, data):
        with open(self.path, 'w', encoding='utf8') as f:
            self.yaml.dump(data, f)


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


def get_uuid(drop=True):
    return str(uuid.uuid1()).replace('-', '') if drop else str(uuid.uuid1())


def write_bs64_img(save_path, data):
    import base64
    with open(save_path, 'wb') as f:
        f.write(base64.b64decode(data))


def hardware_monitor():
    cpu_per = psutil.cpu_percent()
    me_per = psutil.virtual_memory().percent
    return cpu_per, me_per
