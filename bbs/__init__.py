"""
# coding:utf-8
@Time    : 2021/12/06
@Author  : jiangwei
@File    : __init__.py
@Desc    : __init__
@email   : qq804022023@gmail.com
@Software: PyCharm
"""
from flask import Flask, jsonify
from bbs.extensions import db, jwt, cors
from bbs.setting import DevelopmentConfig, ProductionConfig, basedir
from bbs.api.user import user_bp
from bbs.api.auth import auth_bp
from bbs.api.post import post_bp
from bbs.api.normal import normal_bp
from bbs.models import *
import logging
from logging.handlers import RotatingFileHandler


def create_app(config_name=None):
    app = Flask('bbs')
    if config_name is None:
        app.config.from_object(DevelopmentConfig)
    else:
        app.config.from_object(ProductionConfig)
    register_ext(app)
    register_bp(app)
    register_log(app)

    @jwt.expired_token_loader
    def token_expired(jwt_header, jwt_payload):
        """
        token过期的回调函数
        :param jwt_header: jwt token header
        :param jwt_payload: jwt token payload
        :return: 提示信息
        """
        return jsonify(
            code=4003,
            msg='Token已经过期请重新登录！'
        )

    @jwt.invalid_token_loader
    def invalid_token(jwt_header):
        """
        token无效的回调函数
        :param jwt_header: jwt token header
        :return: 提示信息
        """
        return jsonify(
            code=4004,
            msg='无效的Token!'
        )

    return app


def register_ext(app: Flask):
    db.init_app(app)
    jwt.init_app(app)
    cors.init_app(app)


def register_bp(app: Flask):
    app.register_blueprint(user_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(post_bp)
    app.register_blueprint(normal_bp)


def register_log(app: Flask):
    app.logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler = RotatingFileHandler(basedir + '/logs/bbs.log', maxBytes=10 * 1024 * 1024, backupCount=10)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)
    if not app.debug:
        app.logger.addHandler(file_handler)
