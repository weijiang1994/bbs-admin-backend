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
from bbs.models import Post, Notification, User, PostCategory, PostTopic
from bbs.extensions import db
from bbs.constants import NOT_FOUND

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


@post_bp.route('/detail/<post_id>', methods=['GET'])
@jwt_required()
@track_error
def post_detail(post_id):
    post = Post.query.filter_by(id=post_id).first()
    if not post:
        return jsonify(
            code=404,
            msg='未找到相关的帖子!',
            success=True
        )

    return jsonify(
        code=200,
        msg='帖子详情获取成功!',
        success=True,
        data=dict(
            title=post.title,
            author=post.user.username,
            category=post.cats.name,
            c_time=str(post.create_time),
            content=post.content,
        )
    )


@post_bp.route('/review/pass', methods=['POST'])
@jwt_required()
@check_json
@track_error
def review_pass():
    post_id = request.json.get('postId')
    post = Post.query.filter_by(id=post_id).first()
    if not post:
        return jsonify(
            code=404,
            msg='未找到相关的帖子!',
            success=True
        )
    post.status_id = 1
    db.session.commit()
    return jsonify(
        code=200,
        msg='帖子审核成功！',
        success=True
    )


@post_bp.route('/review/fail', methods=['POST'])
@jwt_required()
@check_json
@track_error
def review_fail():
    post_id = request.json.get('postId')
    reason = request.json.get('reason')
    post = Post.query.filter_by(id=post_id).first()
    if not post:
        return jsonify(
            code=404,
            msg='未找到相关的帖子!',
            success=True
        )
    post.status_id = 4
    ntf = Notification(
        type=2,
        target_name='帖子审核',
        send_user='admin',
        receive_id=post.user.id,
        msg=f'<p class="mb-0">新发布的帖子<b>{post.title}</b>审核未通过！</p>'
            f'<p class="mb-0">未通过原因如下：<b>{reason}</b></p>'
    )
    db.session.add(ntf)
    db.session.commit()
    return jsonify(
        code=200,
        msg='帖子审核成功！',
        success=True
    )


@post_bp.route('/list')
@jwt_required()
@track_error
def post_list():
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('size', 20, type=int)
    pagination = Post.query.order_by(Post.create_time.desc()).paginate(page=page, per_page=limit)
    return jsonify(
        render_list(pagination.total, pagination.items, '获取帖子列表成功')
    )


@post_bp.route('/search', methods=['POST'])
@jwt_required()
@check_json
@track_error
def search():
    keyword = request.json.get('keyword')
    category = request.json.get('category')
    if category == 'title':
        posts = Post.query.filter_by(title=keyword).all()
    else:
        posts = Post.query.join(User).filter(User.username == keyword).all()
    if not posts:
        return jsonify(
            code=404,
            msg='没有查询到相关数据！',
            success=True
        )

    return jsonify(
        render_list(len(posts), posts, '查询成功')
    )


@post_bp.route('/batch-block', methods=['POST'])
@jwt_required()
@check_json
@track_error
def batch_ban():
    ids = request.json.get('postIds')
    Post.query.filter(Post.id.in_(ids), Post.status_id == 1).update({'status_id': 2})
    db.session.commit()
    return jsonify(
        code=200,
        msg='批量封禁帖子成功！',
        success=True
    )


@post_bp.route('/batch-unblock', methods=['POST'])
@jwt_required()
@check_json
@track_error
def batch_unblock():
    ids = request.json.get('postIds')
    Post.query.filter(Post.id.in_(ids), Post.status_id == 2).update({'status_id': 1})
    db.session.commit()
    return jsonify(
        code=200,
        msg='批量解封帖子成功！',
        success=True
    )


@post_bp.route('/category/list', methods=['GET'])
@jwt_required()
@track_error
def category_list():
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('size', 20, type=int)
    pagination = PostCategory.query.paginate(page=page, per_page=limit)
    return jsonify(
        render_category_list(pagination.total, pagination.items, msg='获取帖子类别成功!')
    )


@post_bp.route('/category/search', methods=['POST'])
@jwt_required()
@check_json
@track_error
def search_category():
    name = request.json.get('name')
    pc = PostCategory.query.filter_by(name=name).all()
    if not pc:
        return jsonify(
            NOT_FOUND
        )
    return jsonify(
        render_category_list(1, pc)
    )


@post_bp.route('/category/detail', methods=['POST'])
@jwt_required()
@check_json
@track_error
def category_detail():
    category_id = request.json.get('id')
    pc = PostCategory.query.filter_by(id=category_id).first()
    if not pc:
        return jsonify(
            NOT_FOUND
        )
    return jsonify(
        code=200,
        msg='帖子类别详细信息!',
        success=True,
        data=dict(
            name=pc.name,
            topic_id=pc.topic_id,
            desc=pc.desc,
            cate_img=pc.cate_img,
            create_time=str(pc.create_time)
        )
    )


@post_bp.route('/category/edit', methods=['POST'])
@jwt_required()
@check_json
@track_error
def edit_category():
    data = request.json.get('data')
    pt_id = request.json.get('id')
    PostCategory.query.filter_by(id=pt_id).update(data)
    db.session.commit()
    return jsonify(
        code=200,
        msg='类别信息更新成功!',
        success=True
    )


@post_bp.route('/topic/list', methods=['GET'])
@jwt_required()
@track_error
def topic_list():
    page = request.args.get('page', type=int, default=1)
    limit = request.args.get('size', type=int, default=20)
    pagination = PostTopic.query.order_by(PostTopic.c_time.desc()).paginate(page=page, per_page=limit)
    return jsonify(
        render_topic_list(pagination.total, pagination.items)
    )


@post_bp.route('/topic/all', methods=['GET'])
@jwt_required()
@track_error
def all_topic():
    topics = PostTopic.query.all()
    data = []
    for topic in topics:
        data.append(
            dict(
                id=topic.id,
                name=topic.name
            )
        )
    return jsonify(
        code=200,
        msg='所有主题',
        success=True,
        data=data
    )


@post_bp.route('/topic/new', methods=['POST'])
@jwt_required()
@check_json
@track_error
def add_topic():
    name = request.json.get('name')
    if PostTopic.query.filter_by(name=name).first():
        return jsonify(
            code=403,
            msg='已存在相同名称的主题！',
            success=False
        )
    pt = PostTopic(name=name)
    db.session.add(pt)
    db.session.commit()
    return jsonify(
        code=200,
        msg='添加帖子主题成功!',
        success=True
    )


@post_bp.route('/topic/search', methods=['POST'])
@jwt_required()
@check_json
@track_error
def search_topic():
    name = request.json.get('name')
    pt = PostTopic.query.filter_by(name=name).all()
    if not pt:
        return jsonify(
            code=404,
            msg='未找到相关信息！',
            success=True
        )

    return jsonify(
        render_topic_list(1, pt)
    )


@post_bp.route('/topic/edit', methods=['POST'])
@jwt_required()
@check_json
@track_error
def edit_topic():
    topic_id = request.json.get('id')
    name = request.json.get('name')
    origin_topic = PostTopic.query.filter_by(id=topic_id).first()
    new_name_topic = PostTopic.query.filter_by(name=name).first()
    if new_name_topic and new_name_topic.id != origin_topic.id:
        return jsonify(
            code=403,
            msg='当前主题名称已经存在！',
            success=False
        )

    origin_topic.name = name
    db.session.commit()
    return jsonify(
        code=200,
        msg='编辑主题信息成功!',
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
            'status': post.status.name,
            'status_id': post.status_id
        }
        data.append(item)
    ret['data'] = data
    return ret


def render_category_list(total, p_cates, **kwargs):
    ret = dict(
        code=200,
        success=True,
        **kwargs
    )
    data = []
    for p in p_cates:
        data.append(
            dict(
                id=p.id,
                name=p.name,
                topic_id=p.topic_id,
                c_time=str(p.create_time),
                desc=p.desc,
                cate_img=p.cate_img if p.cate_img else '暂无图片',
                topic=p.p_topic.name if p.topic_id else '暂未归类'
            )
        )
    ret['data'] = data
    return ret


def render_topic_list(total, topics, **kwargs):
    ret = dict(
        code=200,
        success=True,
        total=total,
        **kwargs
    )
    data = []
    for topic in topics:
        children = []
        if topic.post_cate:
            for cate in topic.post_cate:
                children.append(
                    dict(
                        id=cate.id,
                        name=cate.name,
                        desc=cate.desc,
                        c_time=str(cate.create_time)
                    )
                )

        data.append(
            dict(
                id=topic.id,
                name=topic.name,
                c_time=str(topic.c_time),
                children=children
            )
        )
    ret['data'] = data
    return ret
