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
from bbs.setting import basedir
import os
import datetime

logger = logging.getLogger()
logger.setLevel(logging.INFO)

log_file = os.path.join(basedir, 'logs', datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
fh = logging.FileHandler(log_file, mode='w')
fh.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
