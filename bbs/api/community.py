"""
# coding:utf-8
@Time    : 2021/12/27
@Author  : jiangwei
@File    : community.py
@Desc    : community
@email   : qq804022023@gmail.com
@Software: PyCharm
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from bbs.decorators import check_json, track_error
from bbs.models import User, Post, Comments

community_bp = Blueprint('community', __name__, url_prefix='/community')


@community_bp.route('/user/info', methods=['GET'])
@jwt_required()
@track_error
def user_info():
    counts = User.query.count()
    return jsonify(
        render_community_info(
            title='用户统计',
            count=counts,
            rooter='当前注册用户数'
        )
    )


@community_bp.route('/post/info', methods=['GET'])
@jwt_required()
@track_error
def post_info():
    count = Post.query.count()
    return jsonify(
        render_community_info(
            title='帖子统计',
            count=count,
            rooter='社区帖子总数'
        )
    )


@community_bp.route('/comment/info', methods=['GET'])
@jwt_required()
@track_error
def comment_info():
    count = Comments.query.count()
    return jsonify(
        render_community_info(
            title='评论统计',
            count=count,
            rooter='社区评论总数'
        )
    )


@community_bp.route('/user/register', methods=['GET'])
@jwt_required()
@track_error
def register_info():
    import datetime
    today = datetime.date.today()
    count = User.query.filter(User.create_time.contains(str(today))).count()
    return jsonify(
        render_community_info(
            title='注册统计',
            count=count,
            rooter='今日注册用户总数'
        )
    )


def render_community_info(title, count, rooter):
    return dict(
        code=200,
        msg='获取社区信息成功!',
        success=True,
        data=dict(
            title=title,
            count=count,
            rooter=rooter
        )
    )
