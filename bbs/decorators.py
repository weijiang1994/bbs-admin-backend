"""
# coding:utf-8
@Time    : 2021/12/06
@Author  : jiangwei
@File    : decorators.py
@Desc    : decorators
@email   : qq804022023@gmail.com
@Software: PyCharm
"""
from flask import request, jsonify
from bbs.setting import basedir
import os


def track_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            return jsonify({'code': 400, 'msg': 'Server Inter Error'})
    return wrapper


def check_json(func):
    """
    Check whether the request data contains JSON
    :param func: decorated function (view function)
    :return: check result
    """

    def wrapper(*args, **kwargs):
        if request.json is None or type(request.json) != dict:
            return jsonify({'code': 422, 'msg': 'Unavailable request data.'})
        return func(*args, **kwargs)

    return wrapper
