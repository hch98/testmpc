

# 查看草稿箱信息
import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from Tool.decorator import check_request, check_page, execute_sql
from article.dao import ArticleDao
from article.models import Type, Article


# 查看草稿箱信息
@csrf_exempt
@check_request('token', 'page')
def queryDraftBox(request):
    json_req = json.loads(request.body)
    token = json_req['token']
    if token == "123456":
        article_count = Article.objects.filter(flag=0).count()
        page = check_page(json_req['page'], article_count)
        sql = ArticleDao.queryDraftBox()
        articles = execute_sql(sql, page)
        json_list = []
        for article in articles:
            json_dict = {"article_id": article[0],
                         "title": article[1],
                         "simple_content": article[2],
                         "page_view": article[3],
                         "create_time": article[4].strftime("%Y年%m月%d日 %H:%M:%S"),
                         "type_name": article[5],
                         "type_id": article[6],
                         "photo_url": article[7],
                         "photo_flag": article[8],
                         }
            json_list.append(json_dict)
        result = {'code': 200, 'article_count': article_count, 'article': json_list}
        return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json")
    result = {'code': 401}
    return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json")


# 编辑草稿
@csrf_exempt
@check_request('token', 'article_id')
def editorDraftBox(request):
    json_req = json.loads(request.body)
    token = json_req['token']
    if token == "123456":
        article_id = json_req['article_id']
        try:
            article = Article.objects.get(article_id=article_id, flag=0)
            type = Type.objects.get(type_id=article.type_id)
            json_list = []
            json_dict = {"article_id": article.article_id,
                         "title": article.title,
                         "content": article.content,
                         "type_id": article.type_id,
                         "type_name": type.type_name
                         }
            json_list.append(json_dict)
            result = {'code': 200, 'comment': json_list}
            return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json")
        except:
            return HttpResponse(json.dumps({'code': 405, 'information': 'sql执行异常！'}))
    result = {'code': 401}
    return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json")
