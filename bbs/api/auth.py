"""
# coding:utf-8
@Time    : 2021/12/07
@Author  : jiangwei
@File    : auth.py
@Desc    : auth
@email   : qq804022023@gmail.com
@Software: PyCharm
"""
from flask import Blueprint, request, jsonify
from bbs.decorators import check_json
from bbs.models import User
from flask_jwt_extended import create_access_token
import datetime

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/login')
@check_json
def login():
    username = request.json.get('username')
    password = str(request.json.get('password'))
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'code': 404, 'msg': '不存在的用户！'})
    if user.status.name == '禁用':
        return jsonify({'code': 402, 'msg': '用户被禁用！'})
    if not user.check_password(password):
        return jsonify({'code': 400, 'msg': '用户名或密码错误！'})
    return jsonify({
        'code': 200,
        'msg': '登录成功!',
        'access_token': create_access_token(username),
        'username': user.username,
        'nickname': user.nickname,
        'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })
