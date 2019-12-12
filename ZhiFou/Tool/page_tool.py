import json


# 分页的工具类
# current_page    当前页码
# per_page        每页的条数
#每次返回每页应该开始的条数start，和每页结束的条数end
class PageInfo(object):
    def __init__(self, current_page, per_page):
        try:
            self.current_page = int(current_page)
        except Exception as e:
            self.current_page = 1
        self.per_page = per_page

    def start(self):
        return (self.current_page - 1) * self.per_page

    def end(self):
        return self.current_page * self.per_page

# 时间的json转换工具
class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, bytes):
            return str(obj, encoding='utf-8')

        return json.JSONEncoder.default(self, obj)