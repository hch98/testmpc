import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django_redis import get_redis_connection

from Tool.decorator import check_request, check_page, execute_sql, check_order
from Tool.page_tool import PageInfo
from article.dao import ArticleDao
from article.dao.ArticleDao import queryPointCount, queryPhotoInfo, queryTypeName

from article.models import Article, Collection, Comment


from comment.dao.CommentDao import queryComentCount

# 首页查询
@csrf_exempt
@check_request('page', 'order_type','user_id')
#@checkToken ("")
def queryArticle(request):
    json_req = json.loads(request.body)

    order = check_order(json_req['order_type'])  # 排序类型默认按时间，0 按时间，1 按阅读数，2 按点赞数
    try:
        article_count = Article.objects.filter(flag=1).count()
    except:
        return HttpResponse(json.dumps({'code': 405, 'information': 'sql执行异常！'}), content_type="application/json")
        page = check_page(json_req['page'], article_count)
        sql = ArticleDao.queryArticle(order)
        articles = execute_sql(sql, 1001, page)
        json_list = []
        for article in articles:
            json_dict = {"article_id": article[0],
                         "title": article[1],
                         "simple_content": article[2],
                         "page_view": queryPageView(article[0]),
                         "create_time": article[4].strftime('%Y{y}%m{m}%d{d}%H:%M:%S').format(y='年', m='月', d='日'),
                         "user_url": article[5],
                         "user_name": article[6],
                         "user_account": article[7],
                         "type_name": article[8],
                         "type_id": article[9],
                         "point_flag": article[10],
                         "point_count": article[11],
                         "photo_url": article[12],
                         "photo_flag": article[13],
                         "comment_count": article[14],
                         }
            json_list.append(json_dict)
        result = {'code': 200, 'article_count': article_count, 'data': json_list}
        return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json")
    result = {'code': 401}
    return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json")



# version 12.12  huangcaihuan
# 查询用户已发帖子
# user_id        登录用户ID
# page           页码
@csrf_exempt
@check_request('user_id', 'page')
#@checkToken ("")
def queryArticleByMyself(request):
    json_req = json.loads(request.body)
    user_id = json_req['user_id']
    page = json_req['page']
    try:
        # 分页查询文章信息
        page_info = PageInfo(page,5)
        articles = Article.objects.filter(user_id=user_id,flag=1)[page_info.start():page_info.end()]

        #单独返回article的全部ID，进行批量操作
        article_ids=list(articles.values_list("article_id",flat=True))
        print(article_ids)
        point_count = queryPointCount(article_ids)     # 获取文章点赞数量
        photo = queryPhotoInfo(article_ids)            # 获取文章图片信息
        comment = queryComentCount(article_ids)        # 获取文章评论的数目
        i=0
        json_list = []
        for article in articles:
            page_view=queryPageView(article.article_id)            #在redis查询浏览量
            type_name=queryTypeName(article.type_id)               #在redis查询文章类型
            json_dict = {"article_id": article.article_id,
                          "title": article.title,
                          "simple_content": article.simple_content,
                          "page_view": page_view,
                          "create_time": article.create_time.strftime('%Y-%m-%d %H:%M:%S'),
                          "type_name": type_name,
                          "type_id": article.type_id,
                          "point":point_count[i],
                          "photo": photo[i],
                          "comment":comment[i]
                         }
            i=i+1
            json_list.append(json_dict)
            print(json_dict)
        result = {'code': 200, 'article_count': len(json_list), 'article': json_list}
        return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json")
    except:
        return HttpResponse(json.dumps({'code': 405, 'information': '执行异常'}), content_type="application/json")




# 分类查询
@csrf_exempt
@check_request('token', 'page', 'type_id', 'order_type')
def queryArticleByTypeId(request):
    json_req = json.loads(request.body)
    token = json_req['token']
    if token == "123456":
        type_id = json_req['type_id']
        order = check_order(json_req['order_type'])
        article_count = Article.objects.filter(type_id=type_id, flag=1).count()
        page = check_page(json_req['page'], article_count)
        sql = ArticleDao.queryArticleByTypeId(order)
        user_id = 1001
        articles = execute_sql(sql, user_id, type_id, page)  # 结果集
        json_list = []
        for article in articles:
            json_dict = {"article_id": article[0],
                         "title": article[1],
                         "simple_content": article[2],
                         "page_view": queryPageView(article[0]),
                         "create_time": article[4].strftime("%Y年%m月%d日 %H:%M:%S"),
                         "user_url": article[5],
                         "user_name": article[6],
                         "user_account": article[7],
                         "point_flag": article[8],
                         "point_count": article[9],
                         "photo_url": article[10],
                         "comment_count": article[11],
                         }
            json_list.append(json_dict)
        result = {'code': 200, 'article_count': article_count, 'data': json_list}
        return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json")
    result = {'code': 401}
    return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json")


# 查看文章详情
@csrf_exempt
@check_request('token', 'article_id')
def queryArticleDetailed(request):
    json_req = json.loads(request.body)
    token = json_req['token']
    if token == "123456":
        loginuser = {
            "user_url": 'http://192.168.195.9:8888/static/images/20191202193207.jpg',
            "user_id": 1001,
            "user_name": '曾琳',
        }
        article_id = json_req['article_id']
        user_id = 1001  # 设定当前用户id为1001
        sql = ArticleDao.queryArticleDetailed()
        articles = execute_sql(sql, user_id, article_id)
        star_count = Collection.objects.filter(user_id=1001).count()
        comment_count = Comment.objects.filter(article_id=article_id).count()
        write_count = Article.objects.filter(user_id=1001).count()
        collection_count = Collection.objects.filter(article_id=article_id).count()
        collect_flag = 0
        if Collection.objects.filter(article_id=article_id, user_id=1001).count() > 0:
            collect_flag = 1
        for article in articles:
            json_dict = {"article_id": article[0],
                         "title": article[1],
                         "content": article[2],
                         "page_view": queryPageView(article[0]),
                         "create_time": article[4].strftime("%Y年%m月%d日 %H:%M:%S"),
                         "user_id": article[5],
                         "user_url": article[6],
                         "user_name": article[7],
                         "user_account": article[8],
                         "point_count": article[9],
                         "type_id": article[10],
                         "type_name": article[11],
                         "point_flag": article[12],
                         "collect_flag": collect_flag,
                         "star_count": star_count,
                         "comment_count": comment_count,
                         "write_count": write_count,
                         "collection_count": collection_count
                         }
        result = {'code': 200, 'user': loginuser, 'article': json_dict}
        return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json")
    result = {'code': 401}
    return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json")


# 用户已收藏文章
@csrf_exempt
@check_request('token', 'user_id', 'page')
def queryCollectionByUserId(request):
    json_req = json.loads(request.body)
    token = json_req['token']
    if token == "123456":
        user_id = json_req['user_id']
        article_count = Collection.objects.filter(user_id=user_id).count()
        page = check_page(json_req['page'], article_count)
        sql = ArticleDao.queryCollectionByUserId()
        articles = execute_sql(sql, user_id, page)  # 结果集
        json_list = []
        for article in articles:
            json_dict = {"article_id": article[0],
                         "title": article[1],
                         "simple_content": article[2],
                         "page_view": queryPageView(article[0]),
                         "create_time": article[4].strftime('%Y{y}%m{m}%d{d}%H:%M:%S').format(y='年', m='月', d='日'),
                         "point_count": article[5],
                         "type_name": article[6],
                         "type_id": article[7],
                         "photo_url": article[8],
                         "photo_flag": article[9],
                         "comment_count": article[10],
                         }
            json_list.append(json_dict)
        result = {'code': 200, 'article_count': article_count, 'article': json_list}
        return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json")
    result = {'code': 401}
    return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json")


# 阅读全文
@csrf_exempt
@check_request('token', 'article_id')
def readFullArticle(request):
    json_req = json.loads(request.body)
    token = json_req['token']
    if token == "123456":
        article = Article.objects.get(article_id=json_req['article_id'])
        result = {'code': 200, 'content': article.content}
        return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json")
    result = {'code': 401, 'information': 'token过期'}
    return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json")


# 浏览量
@csrf_exempt
@check_request('token', 'article_id')
def updatePageView(request):
    json_req = json.loads(request.body)
    token = json_req['token']
    if token == "123456":
        article_id = json_req['article_id']  # 文章ID
        try:
            # 增加浏览量，并且返回浏览量
            page_view = queryPageView(article_id)
            # 修改数据库数据
            Article.objects.filter(article_id=article_id).update(page_view=page_view)
            result = {'code': 200, 'message': "操作成功"}
            return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json")
        except:
            result = {'code': 401, 'information': '发生异常'}
            return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json")
    result = {'code': 401}
    return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json")


# 增加浏览量
def upPageView(article_id):
    try:
        conn = get_redis_connection('default')
        # 先获取key是否存在
        count = conn.hget('article_page_view', article_id)
        # redis不存在该文章的浏览量,则查询数据库数据，然后放进redis
        if count is None:
            article = Article.objects.get(article_id=article_id)
            article.page_view + 1
            article.save(update_fields=['page_view'])
            page_view = article.page_view
            conn.hset('article_page_view', article_id, page_view)
        # redis存在文章的浏览量，则取出数量page_view增加1
        else:
            page_view = int(count.decode('utf-8')) + 1
            conn.hset('article_page_view', article_id, page_view)
    except:
        return "发生异常"
    return page_view


# 返回浏览量
def queryPageView(article_id):
    try:
        conn = get_redis_connection('default')
        # 先获取key是否存在
        count = conn.hget('article_page_view', article_id)
        # redis不存在该文章的浏览量,则查询数据库数据，然后放进redis
        if count is None:
            article = Article.objects.get(article_id=article_id)
            page_view = article.page_view
            conn.hset('article_page_view', article_id, page_view)
        # redis存在文章的浏览量，则取出数量page_view
        else:
            page_view = int(count.decode('utf-8'))
    except:
        return "发生异常"
    return page_view