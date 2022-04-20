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
from flask_jwt_extended import jwt_required, current_user
from bbs.models import User, AdminLog
from bbs.decorators import check_json, track_error
from bbs.extensions import db

user_bp = Blueprint('user', __name__, url_prefix='/user')


@user_bp.route('/batch-ban', methods=['POST'])
@jwt_required()
@check_json
@track_error
def batch_ban():
    usernames = request.json.get('users')
    users = User.query.filter(User.username.in_(usernames)).all()
    disable = 0
    enable = 0
    for user in users:
        if user.status_id == 1:
            user.status_id = 2
            disable += 1
        elif user.status_id == 2:
            user.status_id = 1
            enable += 1
    al = AdminLog(
        admin_id=current_user.id,
        notes='进行了批量封禁/解封操作!'
    )
    db.session.add(al)
    db.session.commit()
    return jsonify(
        code=200,
        msg=f'操作成功，封禁用户{disable}个，解封用户{enable}个！',
        success=True
    )


@user_bp.route('/query', methods=['POST'])
@jwt_required()
@check_json
@track_error
def query():
    category = request.json.get('category')
    keyword = request.json.get('keyword')
    if category == 'username':
        user = User.query.filter(
            User.username == keyword
        ).first()
    else:
        user = User.query.filter(
            User.nickname == keyword
        ).first()
    if not user:
        return jsonify(
            code=404,
            msg='未找到相关信息！'
        )
    return jsonify(table_render(1, [user]))


@user_bp.route('/list', methods=['GET'])
@jwt_required()
@track_error
def user_list():
    page = request.args.get('page', type=int, default=1)
    size = request.args.get('size', type=int, default=20)
    pagination = User.query.order_by(User.create_time.desc()).paginate(page=page, per_page=size)
    users = pagination.items
    return jsonify(table_render(pagination.total, users))


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
    al = AdminLog(
        admin_id=current_user.id,
        notes=f'封禁了用户{user.username}'
    )
    db.session.add(al)
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
    al = AdminLog(
        admin_id=current_user.id,
        notes=f'解封了用户{user.username}'
    )
    db.session.add(al)
    db.session.commit()
    return jsonify(
        code=200,
        msg=f'解封用户{username}成功！',
        success=True
    )


@user_bp.route('/edit', methods=['POST'])
@jwt_required()
@check_json
@track_error
def edit():
    user = request.json.get('user')
    exist_user = User.query.filter_by(id=user.get('id')).first()

    exist_user.gender_id = user.get('gender_id')
    exist_user.role_id = user.get('role_id')
    al = AdminLog(
        admin_id=current_user.id,
        notes=f'编辑了用户{exist_user.username}信息'
    )
    db.session.add(al)
    db.session.commit()
    return jsonify(
        code=200,
        msg='更新用户信息成功！',
        success=True
    )


def table_render(total, users):
    user_dict = {"code": 200, "msg": "网站用户", "count": len(users), "total": total}
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
             'college': user.college.name,
             'role_id': user.role_id,
             'gender_id': user.gender_id
             }
        data.append(s)
    user_dict['data'] = data
    return user_dict
