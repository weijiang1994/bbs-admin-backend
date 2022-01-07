"""
# coding:utf-8
@Time    : 2022/01/07
@Author  : jiangwei
@File    : statistics.py
@Desc    : statistics
@email   : qq804022023@gmail.com
@Software: PyCharm
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from bbs.decorators import check_json, track_error
import requests
from bbs.utils import conf
import urllib.parse

statistics_bp = Blueprint('statistics', __name__, url_prefix='/statistics')
baidu_base_url = 'https://openapi.baidu.com/rest/2.0/tongji/report/getData'
access_token = conf.get('baidu-statistics').get('access-token')
site_id = conf.get('baidu-statistics').get('site-id')


@statistics_bp.route('/district', methods=['POST'])
@jwt_required()
@check_json
@track_error
def district():
    metrics = request.json.get('metrics')
    start_date = request.json.get('start_date')
    end_date = request.json.get('end_date')
    params = dict(
        metrics=metrics,
        start_date=start_date,
        end_date=end_date,
        access_token=access_token,
        site_id=site_id
    )
    district_url = baidu_base_url + '?' + urllib.parse.urlencode(params)
    ret = requests.get(district_url)
    return ret
