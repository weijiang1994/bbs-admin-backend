"""
# coding:utf-8
@Time    : 2021/12/17
@Author  : jiangwei
@File    : post.py
@Desc    : post
@email   : qq804022023@gmail.com
@Software: PyCharm
"""
from flask import Blueprint, request, jsonify
from bbs.decorators import check_json, track_error
from flask_jwt_extended import jwt_required
from bbs.models import Post
from bbs.extensions import db


post_bp = Blueprint('post', __name__, url_prefix='/post')


@post_bp.route('/review/list', methods=['GET'])
@jwt_required()
@track_error
def review_list():
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('size', 20, type=int)
    pagination = Post.query.filter_by(status_id=3).paginate(page=page, per_page=limit)
    posts = pagination.items
    return jsonify(render_list(pagination.total, posts, '待审核的帖子列表！'))


@post_bp.route('/review/batch/pass', methods=['POST'])
@jwt_required()
@check_json
@track_error
def review_batch_pass():
    ids = request.json.get('ids')
    Post.query.filter(Post.id.in_(ids)).update({'status_id': 1})
    db.session.commit()
    return jsonify(
        code=200,
        msg='审核帖子成功！',
        success=True
    )


@post_bp.route('/review/batch/fail', methods=['POST'])
@jwt_required()
@check_json
@track_error
def review_batch_fail():
    ids = request.json.get('ids')
    Post.query.filter(Post.id.in_(ids)).update({'status_id': 4})
    db.session.commit()
    return jsonify(
        code=200,
        msg='审核帖子成功！',
        success=True
    )


def render_list(total, posts, msg, **kwargs):
    ret = {
        'code': 200,
        'msg': msg,
        'success': True,
        'total': total,
        **kwargs
    }
    data = []
    for post in posts:
        item = {
            'id': post.id,
            'author': post.user.username,
            'title': post.title,
            'content': post.textplain,
            'c_time': str(post.create_time),
            'anonymous': post.is_anonymous,
            'category': post.cats.name,
        }
        data.append(item)
    ret['data'] = data
    return ret
