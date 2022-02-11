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
from bbs.models import User, Post, Comments, AdminLog, PostReport
from bbs.utils import hardware_monitor, conf
import os

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


@community_bp.route('/latest/admin-log', methods=['GET'])
@jwt_required()
@track_error
def latest_log():
    logs = AdminLog.query.order_by(AdminLog.timestamps.desc()).limit(8)
    ret = dict(
        code=200,
        msg='获取最近管理员操作记录成功!',
        success=True
    )
    data = []
    for log in logs:
        data.append(
            dict(
                content=log.admin_user.username + log.notes,
                timestamp=str(log.timestamps)
            )
        )
    ret['data'] = data
    return jsonify(ret)


@community_bp.route('/server-status', methods=['GET'])
@jwt_required()
@track_error
def server_status():
    cpu, mem = hardware_monitor()
    return jsonify(
        code=200,
        data=dict(
            cpu=cpu,
            mem=mem
        )
    )


@community_bp.route('/report/unread', methods=['GET'])
@jwt_required()
@track_error
def report_unread():
    page = request.args.get('page', default=1, type=int)
    limit = request.args.get('size', default=1, type=int)
    prs = PostReport.query.filter_by(flag=0).paginate(page=page, per_page=limit)
    return jsonify(render_report_info(prs.items, prs.total))


@community_bp.route('/report/read', methods=['GET'])
@jwt_required()
@track_error
def report_read():
    page = request.args.get('page', default=1, type=int)
    limit = request.args.get('size', default=1, type=int)
    prs = PostReport.query.filter_by(flag=1).paginate(page=page, per_page=limit)
    return jsonify(render_report_info(prs.items, prs.total))


def render_report_info(prs, total, **kwargs):
    post_base_url = conf.get('frontend_url') + conf.get('post_base_url')
    ret = dict(
        code=200,
        msg='获取举报信息成功!',
        success=True,
        total=total
    )
    data = []
    for pr in prs:
        data.append(dict(
            post_title=pr.post.title,
            post_url=os.path.join(post_base_url, str(pr.post_id)),
            report_body=pr.rep_content,
            report_tag=pr.report_cate.name,
            c_time=str(pr.timestamps)
        ))
    ret['data'] = data
    return ret


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
