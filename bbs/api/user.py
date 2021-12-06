"""
# coding:utf-8
@Time    : 2021/12/06
@Author  : jiangwei
@File    : user.py
@Desc    : user
@email   : qq804022023@gmail.com
@Software: PyCharm
"""
from flask import Blueprint, jsonify
user_bp = Blueprint('user', __name__, url_prefix='/user')


@user_bp.route('/get-user', methods=['GET'])
def get_user():
    users = User.query.filter_by(role=1).all().as_dict()
    return jsonify(users)
