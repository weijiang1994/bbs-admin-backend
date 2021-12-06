"""
# coding:utf-8
@Time    : 2021/12/06
@Author  : jiangwei
@File    : __init__.py
@Desc    : __init__
@email   : qq804022023@gmail.com
@Software: PyCharm
"""
from flask import Flask
from app.extensions import db, login_manager
from app.setting import DevelopmentConfig, ProductionConfig


def create_app(config_name=None):
    app = Flask('bbs-admin-backend')
    if not config_name:
        app.config.from_object(DevelopmentConfig)
    else:
        app.config.from_object(ProductionConfig)
    return app


def register_ext(app: Flask):
    db.init_app(app)
    login_manager.init_app(app)


def register_bp():
    pass
