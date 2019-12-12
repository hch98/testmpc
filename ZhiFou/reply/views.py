import json

from django.db import connection
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from Tool.decorator import check_request, check_page

from Tool.page_tool import PageInfo
from article.models import Reply, User


# 删除回复
# reply_id  回复ID
#  根据回复的ID进行软删除，把标志位改为0
from users.utils.user_info import queryUserInfo


@csrf_exempt
@check_request( 'reply_id')
#@checkToken ("")
def deleteReply(request):
    json_req = json.loads(request.body)
    reply_id = json_req['reply_id']
    try:
        r = Reply.objects.filter(reply_id=reply_id).update(is_delete=0)
        if r == 1:
            return HttpResponse(json.dumps({'code': 200 }, ensure_ascii=False), content_type="application/json")
    except:
        return HttpResponse(json.dumps({'code': 405, 'information': '执行异常'}), content_type="application/json")

#展开评论的所有回复
# comment_id      评论的ID号
# page            页码
#分页查询评论下的所有回复
@csrf_exempt
@check_request('comment_id','page')
def queryReply(request):
    json_req = json.loads(request.body)
    comment_id = json_req['comment_id']
    page = json_req['page']
    try:
        #分页查询,每页5条
        page_info = PageInfo(page,5)
        replyList = Reply.objects.filter(comment_id=comment_id,is_delete=1).order_by('-create_time')[page_info.start():page_info.end()]

        # 单独返回from_user的全部id，进行批量操作
        from_user_ids = list(replyList.values_list("from_user_id", flat=True))
        from_user = queryUserInfo(from_user_ids)

        # 单独返回to_user的全部id，进行批量操作
        to_user_ids = list(replyList.values_list("to_user_id", flat=True))
        to_user = queryUserInfo(to_user_ids)
        i=0
        json_list = []
        for reply in replyList:
            json_dict = {"rely_id": reply.reply_id,
                         "reply_content": reply.reply_content,
                         "create_time": reply.create_time.strftime('%Y-%m-%d %H:%M:%S'),
                         "from_user": from_user[i],
                         "to_user": to_user[i]
                         }
            i=i+1
            json_list.append(json_dict)
        result = {'code': 200, 'reply': json_list}
        return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json")
    except:
        return HttpResponse(json.dumps({'code': 405, 'information': '执行异常'}), content_type="application/json")


# 回复给评论，用户可以对文章的评论进行回复
#comment_id     回复的评论ID
#from_user_id   回复目标用户
#reply_content  回复内容
#user_id        登录用户ID
@csrf_exempt
@check_request('comment_id', 'from_user_id', 'reply_content','user_id')
#@checkToken ("")
def addReplyToComment(request):
    json_req = json.loads(request.body)
    comment_id = json_req['comment_id']
    from_user_id=json_req['from_user_id']
    reply_content=json_req['reply_content']
    user_id = json_req['user_id']
    try:
        if len(reply_content) > 100:
             result = {'code': 406, 'information': '字数超过限制'}
             return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json")
        else:
            login_user = User.objects.get(user_id=user_id)
            # 先获取一个目标用户对象
            from_user_id = User.objects.get(user_id=from_user_id)
            # 创建回复
            reply = Reply.objects.create(comment_id=comment_id,from_user_id=user_id,to_user=from_user_id,reply_content=reply_content)
            json_list = []
            json_dict = {"reply_id": reply.reply_id,
                         "reply_content": reply.reply_content,
                         "create_time": reply.create_time.strftime('%Y-%m-%d %H:%M:%S'),
                         "from_user_id": login_user.user_id,
                         "from_user_name": login_user.user_name,
                         "from_user_url": login_user.user_url,
                         "to_user_id":from_user_id.user_id,
                         "to_user_name": from_user_id.user_name,
                         "to_user_url": from_user_id.user_url
                         }
            json_list.append(json_dict)
        result = {'code': 200, 'reply_comment': json_list}
        return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json")
    except:
        return HttpResponse(json.dumps({'code': 405, 'information': '执行异常'}), content_type="application/json")



# 多重回复
#comment_id     回复的评论ID
#from_user_id   回复目标用户
#reply_content  回复内容
#user_id        登录用户ID
@csrf_exempt
@check_request('reply_id','comment_id','from_user_id','reply_content','user_id')
#@checkToken ("")
def addReplyToReply(request):
    json_req = json.loads(request.body)
    target_id = json_req['reply_id']
    comment_id = json_req['comment_id']
    from_user_id=json_req['from_user_id']
    reply_content=json_req['reply_content']
    user_id = json_req['user_id']
    try:
        if len(reply_content) > 100:
            result = {'code': 406, 'information': '字数超过限制'}
            return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json")
        else:
            login_user = User.objects.get(user_id=user_id)
            #先获取一个目标用户对象
            from_user_id = User.objects.get(user_id=from_user_id)
            # 插入回复
            reply = Reply.objects.create(comment_id=comment_id,target_id=target_id,from_user_id=user_id,to_user=from_user_id,reply_content=reply_content)
            json_list = []
            json_dict = {"reply_id": reply.reply_id,
                         "reply_content": reply.reply_content,
                          "create_time": reply.create_time.strftime('%Y{y}%m{m}%d{d}%H:%M:%S').format(y='年', m='月', d='日'),
                          "from_user_id": login_user.user_id,
                          "from_user_name": login_user.user_name,
                          "from_user_url": login_user.user_url,
                          "to_user_id": from_user_id.user_id,
                          "to_user_name": from_user_id.user_name,
                          "to_user_url": from_user_id.user_url
                        }
            json_list.append(json_dict)
            result = {'code': 200, 'reply_reply': json_list}
            return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json")
    except:
        return HttpResponse(json.dumps({'code': 405, 'information': '执行异常'}), content_type="application/json")