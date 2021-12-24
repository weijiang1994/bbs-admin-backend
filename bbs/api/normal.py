"""
# coding:utf-8
@Time    : 2021/12/24
@Author  : jiangwei
@File    : tool.py
@Desc    : tool
@email   : qq804022023@gmail.com
@Software: PyCharm
"""
from flask import Blueprint, request, jsonify, send_from_directory, url_for
from bbs.extensions import db
from bbs.decorators import check_json, track_error
from flask_jwt_extended import jwt_required
from bbs.models import PostCategory
from bbs.utils import conf, get_uuid, write_bs64_img
import os

normal_bp = Blueprint('tool', __name__, url_prefix='/normal')


@normal_bp.route('/upload-image', methods=['POST'])
@jwt_required()
@check_json
@track_error
def upload_img():
    file = request.json.get('bs64')
    category_id = request.json.get('categoryId')
    bs64 = file.split(',')
    suffix = bs64[0].split('/')[-1].split(';')[0]
    data = bs64[-1]
    if category_id != '':
        save_root = os.path.join(conf.get('category_path'), category_id)
        if not os.path.exists(save_root):
            os.mkdir(save_root)
    else:
        save_root = os.path.join(conf.get('category_path'))
    image_name = get_uuid() + '.' + suffix
    write_bs64_img(os.path.join(save_root, image_name), data)

    return jsonify(
        code=200,
        msg='上传成功!',
        success=True,
        filename=image_name,
        img_url=url_for('.get_category_image', cate_id=category_id, image_name=image_name) if category_id else
        url_for('.temp_image', image_name=image_name)
    )


@normal_bp.route('/category-image/<cate_id>/<image_name>', methods=['GET'])
@track_error
def get_category_image(cate_id, image_name):
    filename = image_name
    path = os.path.join(conf.get("category_path"), cate_id)
    return send_from_directory(path, filename)


@normal_bp.route('/temp-image/<image_name>')
@track_error
def temp_image(image_name):
    filename = image_name
    path = conf.get('category_path')
    return send_from_directory(path, filename)
