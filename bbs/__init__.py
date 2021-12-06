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
from bbs.extensions import db
from bbs.setting import DevelopmentConfig, ProductionConfig
from bbs.api.user import user_bp
from bbs.models import *


def create_app(config_name=None):
    app = Flask('bbs')
    if not config_name:
        app.config.from_object(DevelopmentConfig)
    else:
        app.config.from_object(ProductionConfig)
    register_ext(app)
    register_bp(app)
    return app


def register_ext(app: Flask):
    db.init_app(app)


def register_bp(app: Flask):
    app.register_blueprint(user_bp)

