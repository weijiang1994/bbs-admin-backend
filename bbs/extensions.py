"""
# coding:utf-8
@Time    : 2021/12/06
@Author  : jiangwei
@File    : extensions.py
@Desc    : extensions
@email   : qq804022023@gmail.com
@Software: PyCharm
"""
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_login import LoginManager

db = SQLAlchemy()
jwt = JWTManager()
