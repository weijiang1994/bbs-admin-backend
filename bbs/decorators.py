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


def track_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            pass

    return wrapper


@track_error
def check_json(func):
    """
    Check whether the request data contains JSON
    :param func: decorated function (view function)
    :return: check result
    """

    def wrapper(*args, **kwargs):
        try:
            request.json
            return func(*args, **kwargs)
        except Exception as e:
            return jsonify({'code': 422, 'msg': 'Unavailable request data.'})

    return wrapper
