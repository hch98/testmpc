import json
import re
from builtins import len

from django.http import HttpResponse
from django.utils.datetime_safe import datetime
from django.views.decorators.csrf import csrf_exempt

from Tool.decorator import check_request

from article.models import Article, User, Point


# 保存文章（发表文章或者保存草稿）
@csrf_exempt
@check_request('token', 'article_id', 'title', 'content', 'type_id', 'flag')
def saveArticle(request):
    json_req = json.loads(request.body)
    token = json_req['token']
    if token == "123456":
        article_id = json_req['article_id']  # 文章ID
        title = json_req['title']  # 文章标题
        if len(title) > 50:
            result = {'code': 406, 'information': '字数超过限制！'}
            return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json")
        type_id = json_req['type_id']  # 文章类型
        flag = json_req['flag']  # 草稿 or 发布
        content = json_req['content']  # 文章内容
        dr = re.compile(r'<[^>]+>', re.S)
        filter_content = dr.sub('', content)
        try:
            # 获取登录用户ID
            login_user = User.objects.get(user_id=1001)
            # 获得过滤标签后filter_content的字数
            a = len(filter_content)
            # content的字数大于100则截取作为简介，否则就直接作为简介存储
            if a > 100:
                simple_content = filter_content[0:100]
            else:
                simple_content = filter_content
            # flag=1,发布文章
            if flag == 1:
                # 发表文章
                article = Article(article_id=article_id, user_id=login_user, title=title, simple_content=simple_content,
                                  create_time=datetime.now(), content=content, type_id=type_id, flag=1)
                article.save()
                # 插入文章点赞数量
                point = Point(article_id=article_id, point_count=0)
                point.save()
            # flag=0,保存草稿
            else:
                article = Article(article_id=article_id, user_id=login_user, title=title, simple_content=simple_content,
                                  create_time=datetime.now(), content=content, type_id=type_id, flag=0)
                article.save()
            result = {'code': 200}
            return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json")
        except:
            return HttpResponse(json.dumps({'code': 405, 'information': 'sql执行异常！'}), content_type="application/json")
    result = {'code': 401}
    return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json")


# 删除文章或者草稿
@csrf_exempt
@check_request('token', 'article_id')
def delArticleOrDraft(request):
    json_req = json.loads(request.body)
    token = json_req['token']
    if token == "123456":
        article_id = json_req['article_id']  # 回复的ID
        try:
            article = Article.objects.filter(article_id=article_id).update(flag=2)
            if article > 0:
                result = {'code': 200}
                return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json")
        except:
            return HttpResponse(json.dumps({'code': 405, 'information': 'sql执行异常！'}))
    result = {'code': 401}
    return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json")


# 生成文章ID
@csrf_exempt
@check_request('token', 'type_id', )
def createArticleId(request):
    json_req = json.loads(request.body)
    token = json_req['token']
    if token == "123456":
        type_id = json_req['type_id']
        try:
            # 获取登录用户ID
            login_user = User.objects.get(user_id=1001)
            # 先查询是否已经存在articleID
            article = Article.objects.filter(user_id=login_user, flag=3, title="")
            # article 已经存在则直接返回
            if article.exists():
                result = {'code': 200, 'article_id': article[0].article_id}
                return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json")
            # 不存在则创建
            else:
                # 创建article对象
                article = Article(user_id=login_user, type_id=type_id, flag=3)
                # 保存文章
                article.save()
                result = {'code': 200, 'article_id': article.article_id}
                return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json")
        except:
            return HttpResponse(json.dumps({'code': 405}))
    result = {'code': 401}
    return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json")



