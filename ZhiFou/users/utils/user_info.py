import json

from django.http import HttpResponse

from users.models import User


# 通过user_id获取用户信息
# 返回用户信息JSON字符串
def get_user_info(user_id):
    try:
        user = User.objects.get(user_id=user_id)
    except:
        return HttpResponse(json.dumps({'code':'4001'}))    # 用户不存在
    return HttpResponse (json.dumps ({
        'code': 200,
        'user_id': user.user_id,
        'user_url': user.user_url,
        'user_name': user.user_name,
        # 'user_account': user.user_account,
        # 'user_gender': user.user_gender,
        # 'email': user.email,
        # 'user_phone': user.user_phone,
        # 'user_credit': user.user_credit,
        # 'status':user.status
    }))

#  Version 12.12
# 批量获取用户信息的接口
def queryUserInfo(users):
    json_list=[]
    for i in users:
        user = User.objects.get(user_id=i)
        dic={
            "user_id":user.user_id,"user_name":user.user_name,"user_url":user.user_url}
        json_list.append(dic)
    return json_list