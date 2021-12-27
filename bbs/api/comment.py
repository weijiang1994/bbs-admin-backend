"""
# coding:utf-8
@Time    : 2021/12/27
@Author  : jiangwei
@File    : comment.py
@Desc    : comment
@email   : qq804022023@gmail.com
@Software: PyCharm
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from bbs.decorators import track_error, check_json
from bbs.models import Comments, User
from bbs.extensions import db
from bbs.constants import NOT_FOUND

comment_bp = Blueprint('comment', __name__, url_prefix='/comment')


@comment_bp.route('/list', methods=['GET'])
@jwt_required()
@track_error
def comment_list():
    page = request.args.get('page', default=1, type=int)
    limit = request.args.get('size', default=20, type=int)
    pagination = Comments.query.paginate(page=page, per_page=limit)
    return jsonify(
        render_comment(pagination.total, pagination.items, msg='获取评论列表成功!', success=True)
    )


@comment_bp.route('/search', methods=['POST'])
@jwt_required()
@check_json
@track_error
def search():
    keyword = request.json.get('keyword')
    category = request.json.get('category')
    if category == 'author':
        comments = Comments.query.join(User).filter(User.username == keyword).all()
    else:
        comments = Comments.query.filter(Comments.body.contains(keyword)).all()
    if not comments:
        return jsonify(
            NOT_FOUND
        )
    return jsonify(
        render_comment(len(comments), comments)
    )


@comment_bp.route('/delete', methods=['POST'])
@jwt_required()
@check_json
@track_error
def delete():
    comment_id = request.json.get('commentId')
    comment = Comments.query.filter_by(id=comment_id).first()
    comment.delete_flag = 1
    db.session.commit()
    return jsonify(
        code=200,
        msg='屏蔽评论操作成功！',
        success=True
    )


@comment_bp.route('/batch/delete', methods=['POST'])
@jwt_required()
@check_json
@track_error
def delete_batch():
    comment_ids = request.json.get('commentIds')
    Comments.query.filter(Comments.id.in_(comment_ids)).update({'delete_flag': 1})
    db.session.commit()
    return jsonify(
        code=200,
        msg="批量屏蔽评论操作成功!",
        success=True
    )


@comment_bp.route('/batch/release', methods=['POST'])
@jwt_required()
@check_json
@track_error
def release_batch():
    comment_ids = request.json.get('commentIds')
    Comments.query.filter(Comments.id.in_(comment_ids)).update({'delete_flag': 0})
    db.session.commit()
    return jsonify(
        code=200,
        msg="批量显示评论操作成功!",
        success=True
    )


@comment_bp.route('/release', methods=['POST'])
@jwt_required()
@check_json
@track_error
def release():
    comment_id = request.json.get('commentId')
    comment = Comments.query.filter_by(id=comment_id).first()
    comment.delete_flag = 0
    db.session.commit()
    return jsonify(
        code=200,
        msg='显示评论操作成功！',
        success=True
    )


def render_comment(total, comments, **kwargs):
    ret = dict(
        code=200,
        total=total,
        **kwargs
    )
    data = []
    for comment in comments:
        data.append(
            dict(
                id=comment.id,
                author=comment.author.username,
                body=comment.body,
                c_time=str(comment.timestamps),
                post=comment.post.title,
                delete_flag=comment.delete_flag
            )
        )
    ret['data'] = data
    return ret
