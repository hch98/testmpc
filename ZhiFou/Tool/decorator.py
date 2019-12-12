import json
from math import ceil

from django.db import connection
from django.http import HttpResponse


# 装饰器，检查request参数是否齐全
def check_request(*params):
    def __check_request(func):
        def warpper(request):
            print(params)
            if request.method != 'POST':
                result = {'code': 402, 'information': '请求方式错误！'}
                return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json")
            for param in params:
                try:
                    json_req = json.loads(request.body)[param]
                    if type(json_req) is str:
                        if json_req.strip() == "":
                            data = {'code': 501, 'information': '空参数异常！', }
                            return HttpResponse(json.dumps(data), content_type="application/json")
                    if type(json_req) is int:
                        if json_req < 0:
                            data = {'code': 501, 'information': '参数不能为负数！', }
                            return HttpResponse(json.dumps(data), content_type="application/json")
                except KeyError:
                    data = {'code': 501, 'information': '缺少参数异常！', }
                    return HttpResponse(json.dumps(data), content_type="application/json")
            # 参数都存在，则继续执行
            return func(request)
        return warpper
    return __check_request


# 校验page
def check_page(page, count):
    if type(page) is not int:
        result = {'code': 405, 'information': '参数类型异常！'}
        return HttpResponse(json.dumps(result), content_type="application/json")
    if page <= 0:
        return 0
    # 每页至少十条记录
    if count > 10:
        if page > ceil(count / 10):
            return ceil(count/10)-1
    return page-1


# 返回order
def check_order(order_type):
    order = "order by t1.create_time desc"
    if order_type == 0:
        order = "order by t1.create_time desc"
    if order_type == 1:
        order = "order by t1.page_view desc"
    if order_type == 2:
        order = "order by t1.point_count desc"
    return order


# 返回服务器IP地址
def toIp():
    return "192.168.195.9:8123"


# 执行sql
def execute_sql(sql, *args):
    try:
        cur = connection.cursor()
        cur.execute(sql, args)
        list = cur.fetchall()
    except:
        return HttpResponse(json.dumps({'code': 405, 'information': 'sql执行异常！'}), content_type="application/json")
    finally:
        cur.close
    return list



def toJson(querys, *params):
    i = 0
    json_list = []
    for query in querys:
        json_dict = {}
        for i in range(len(params)):
            if params[i] == "create_time":
                query[i] = query[i].strftime("%Y年%m月%d日 %H:%M:%S")
            json_dict[params[i]] = query[i]
        i = 0
        json_list.append(json_dict)
    return json_list

















