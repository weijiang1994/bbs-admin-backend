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
from bbs.models import VisitStatistic, CommentStatistic, PostStatistic, SearchStatistic
import datetime

statistics_bp = Blueprint('statistics', __name__, url_prefix='/statistics')
baidu_base_url = 'https://openapi.baidu.com/rest/2.0/tongji/report/getData'
access_token = conf.get('baidu-statistics').get('access-token')
site_id = conf.get('baidu-statistics').get('site-id')


def render_traffic(key, datas):
    data = []
    for d in datas:
        data.append(d.times)
    return dict(
        name=key,
        type='line',
        stack='总量',
        data=data
    )


@statistics_bp.route('/index', methods=['GET'])
def statistic():
    keys = ['访问', '评论', '发帖', '搜索']
    date_range = request.args.get('dateRange', default='week', type=str)
    today = datetime.date.today()
    if date_range == 'week':
        start_date = today - datetime.timedelta(days=7)
    elif date_range == 'half':
        start_date = today - datetime.timedelta(days=15)
    else:
        start_date = today - datetime.timedelta(days=30)
    vs = VisitStatistic.query.filter(VisitStatistic.day > start_date).all()
    cs = CommentStatistic.query.filter(CommentStatistic.day > start_date).all()
    ps = PostStatistic.query.filter(PostStatistic.day > start_date).all()
    ss = SearchStatistic.query.filter(SearchStatistic.day > start_date).all()
    series = []
    dates = []
    for idx, st in enumerate([vs, cs, ps, ss]):
        series.append(render_traffic(keys[idx], st))
    for v in vs:
        dates.append(str(v.day))
    return dict(
        code=200,
        success=True,
        series=series,
        dates=dates
    )


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
