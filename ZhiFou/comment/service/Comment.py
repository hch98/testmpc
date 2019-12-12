

import json
from builtins import len

from django.http import HttpResponse
from django.utils.datetime_safe import datetime
from django.views.decorators.csrf import csrf_exempt

from Tool.decorator import check_request, check_page, execute_sql
from article.models import User, Comment


# 发表评论
from comment.dao import CommentDao
from users.utils.token_op import checkToken


#发表评论
#comment_content  评论的内容
#article_id       文章ID
#user_id          登录用户
#先判断评论内容的长度，限制100字以内，字数超出限制则不予发表
@csrf_exempt
@check_request('comment_content', 'article_id','user_id')
#@checkToken ("")
def addComment(request):
    json_req = json.loads(request.body)
    comment_content = json_req['comment_content']
    article_id = json_req['article_id']
    user_id = json_req['user_id']
    try:
        if len(comment_content) > 100:
            return HttpResponse(json.dumps( result = {'code': 406, 'information': '字数超过限制'}, ensure_ascii=False), content_type="application/json")
        else:
            login_id = User.objects.get(user_id=user_id)
            # 插入评论信息
            comment = Comment.objects.create(comment_content=comment_content, article_id=article_id, create_time=datetime.now(), user_id=user_id)
            json_list = []
            json_dict = {"comment_id": comment.comment_id,
                          "comment_content": comment.comment_content,
                          "create_time": comment.create_time.strftime('%Y年%m月%d日 %H:%M:%S'),
                          "user_id": login_id.user_id,
                          "user_name": login_id.user_name,
                          "user_url": login_id.user_url,
                        }
            json_list.append(json_dict)
            result = {'code': 200, 'comment': json_list}
            return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json")
    except:
        return HttpResponse(json.dumps({'code': 405, 'information': '执行异常'}), content_type="application/json")


# 删除评论
# comment_id  评论ID
#  根据评论的ID进行软删除，把标志位改为0
@csrf_exempt
@check_request('comment_id')
#@checkToken ("")
def deleteComment(request):
    json_req = json.loads(request.body)
    comment_id = json_req['comment_id']
    try:
        r = Comment.objects.filter(comment_id=comment_id).update(is_delete=0)
        if r == 1:
            return HttpResponse(json.dumps({'code': 200}, ensure_ascii=False), content_type="application/json")
    except:
        return HttpResponse(json.dumps({'code': 405, 'information': '执行异常'}), content_type="application/json")


# 查看评论
# article_id  文章ID号
# user_id     用户ID
# page        页码
# 根据文章ID查询该文章的所有评论，返回评论信息和登录用户信息
@csrf_exempt
@check_request('article_id', 'user_id','page')
#@checkToken ("")
def queryComment(request):
    json_req = json.loads(request.body)
    user_id = json_req['user_id']
    article_id = json_req['article_id']
    try:
        comment_count = Comment.objects.filter(article_id=article_id, is_delete=1).count()
        page = check_page(json_req['page'], comment_count)
        sql = CommentDao.queryComment
        comments = execute_sql(sql, article_id, page)
        json_list = []
        for comment in comments:
            json_dict = {"comment_id": comment[0],
                         "comment_content": comment[1],
                         "create_time": comment[2].strftime("%Y年%m月%d日 %H:%M:%S"),
                         "user_id": comment[3],
                         "user_name": comment[4],
                         "user_url": comment[5]
                         }
            json_list.append(json_dict)
        result = {'code': 200, "loginuser": user_id, 'comment_count': comment_count, 'comment': json_list}
        return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json")
    except:
        return HttpResponse(json.dumps({'code': 405, 'information': '执行异常'}, ensure_ascii=False), content_type="application/json")