"""
# coding:utf-8
@Time    : 2021/12/06
@Author  : jiangwei
@File    : user.py
@Desc    : user
@email   : qq804022023@gmail.com
@Software: PyCharm
"""
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from bbs.models import User
from bbs.decorators import check_json, track_error
from bbs.extensions import db

user_bp = Blueprint('user', __name__, url_prefix='/user')


@user_bp.route('/list', methods=['GET'])
@jwt_required()
@track_error
def user_list():
    page = request.args.get('page', type=int, default=1)
    size = request.args.get('size', type=int, default=20)
    pagination = User.query.paginate(page=page, per_page=size)
    users = pagination.items
    return jsonify(table_render(pagination, users))


@user_bp.route('/ban', methods=['POST'])
@jwt_required()
@check_json
def ban():
    username = request.json.get('username')
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify(
            code=404,
            msg='不存在的用户！',
            success=False
        )
    user.status_id = 2
    db.session.commit()
    return jsonify(
        code=200,
        msg=f'封禁用户{username}成功！',
        success=True
    )


@user_bp.route('/unban', methods=['POST'])
@jwt_required()
@check_json
def unban():
    username = request.json.get('username')
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify(
            code=404,
            msg='不存在的用户！',
            success=False
        )
    user.status_id = 1
    db.session.commit()
    return jsonify(
        code=200,
        msg=f'解封用户{username}成功！',
        success=True
    )


@user_bp.route('/add-user', methods=['POST'])
def add_user():
    username = request.json.get('username')
    nickname = request.json.get('nickname')
    email = request.json.get('email')
    tag = 0
    if User.query.filter_by(username=username).first():
        info = '用户名已存在'
    elif User.query.filter_by(nickname=nickname).first():
        info = '昵称已存在'
    elif User.query.filter_by(email=email).first():
        info = '邮箱已经被注册'
    else:
        password = request.json.get('password')
        gender = request.json.get('gender')
        role = request.json.get('role')
        college = request.json.get('college')
        user = User(username=username,
                    nickname=nickname,
                    email=email,
                    gender_id=gender,
                    role_id=role,
                    status_id=1,
                    college_id=college)
        user.generate_avatar()
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        r = Role.query.filter_by(id=role).first()
        log = AdminLog(admin_id=current_user.id,
                       target_id=user.id,
                       op_id=4,
                       notes='添加了用户{},角色为{}'.format(user.username, r.name))
        db.session.add(log)
        db.session.commit()
        tag = 1
        info = '添加用户成功!'
    return jsonify({'tag': tag, 'info': info})


def table_render(pagination, users):
    user_dict = {"code": 200, "msg": "网站用户", "count": len(users), "total": pagination.total}
    data = []
    for user in users:
        s = {'id': user.id,
             'username': user.username,
             'nickname': user.nickname,
             'city': user.location,
             'slogan': user.slogan,
             'website': user.website,
             'join': str(user.create_time),
             'role': user.role.name,
             'email': user.email,
             'status': user.status_id,
             'gender': user.gender.name,
             'college': user.college.name}
        data.append(s)
    user_dict['data'] = data
    return user_dict
