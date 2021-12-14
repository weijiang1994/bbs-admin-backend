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
from flask_jwt_extended import create_access_token, current_user, jwt_required, get_jwt_identity, create_refresh_token, \
    set_access_cookies, unset_access_cookies
import datetime
from bbs.extensions import jwt
from bbs.utils import conf

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/login', methods=['POST'])
@check_json
def login():
    username = request.json.get('username')
    password = str(request.json.get('password'))
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify(
            code=404,
            msg='用户不存在！',
            success=False
        )

    if user.status.name == '禁用':
        return jsonify(
            code=403,
            msg='用户已被禁用！',
            success=False
        )

    if not user.check_password(password):
        return jsonify(
            code=400,
            msg='用户名或密码错误！',
            success=False
        )

    if user.role_id != 1:
        return jsonify(
            code=403,
            msg='非管理员禁止登录！',
            success=False
        )

    access_token = create_access_token(identity=user, additional_claims={'admin': True})
    response = jsonify(
        code=200,
        msg='登录成功！',
        userid=user.id,
        username=user.username,
        nickname=user.nickname,
        timestamp=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        access_token=access_token,
        success=True
    )
    set_access_cookies(response, access_token)
    return response


@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.id


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data['sub']
    return User.query.filter_by(id=identity).one_or_none()


@auth_bp.route('/userInfo')
@jwt_required()
def user_info():
    return jsonify(
        id=current_user.id,
        username=current_user.username,
        nickname=current_user.nickname,
        avatar=conf.get('frontend_url') + current_user.avatar
    ), 200


@auth_bp.route('/logout')
@jwt_required()
def logout():
    response = jsonify(
        code=200,
        msg='注销成功！'
    )
    unset_access_cookies(response)
    return response
