import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from users.models import User
from users.utils.token_op import get_userid, checkToken

# 通过邮件链接修改密码
@csrf_exempt
def reset_password_by_email(request, token):
    print(token)
    if request.method ==  'POST':
        # 解token 查找用户
        user_id = get_userid (token)
        user =  User.objects.get(user_id=user_id)
        json_req = json.loads (request.body)
        password = json_req['password']
        re_password = json_req['re_password']
        try:
            user = User.objects.get (user_id=user_id)
        except:
            return HttpResponse (json.dumps ({'code': 401}))  # 用户不存在
        if re_password == password:  # 验证两次密码是否相同
            user.set_password (password)
            user.save ()
            return HttpResponse (json.dumps ({
                'code': 200,
                'user_id': user.user_id,
                'user_account': user.user_account,
                'user_url': user.user_url,
                'user_name': user.user_name,
                'user_gender': user.user_gender,
                'email': user.email,
                'user_phone': user.user_phone,
                'user_credit': user.user_credit
            })) # 修改成功
        else:
            return HttpResponse (json.dumps ({'code': 402}))  # 两次密码不相同
    else:
        return HttpResponse (json.dumps ({'code': 404}))  # 请求非post


# 修改密码
@csrf_exempt
@checkToken ("")
def reset_password(request):
    if request.method == 'POST':
        json_req = json.loads (request.body)
        user_id = json_req['user_id']  # 如果用多个request.POST['user_id']会报错MultiValueDictKeyError(key),这是表单类型
        password = json_req['password']
        re_password = json_req['re_password']
        try:
            user = User.objects.get (user_id=user_id)
        except:
            return HttpResponse (json.dumps ({'code': 401}))  # 用户不存在
        if re_password == password:  # 验证两次密码是否相同
            user.set_password (password)
            user.save ()
            return HttpResponse (json.dumps ({'code': 200}))  # 修改成功
        else:
            return HttpResponse (json.dumps ({'code': 402}))  # 两次密码不相同
    else:
        return HttpResponse (json.dumps ({'code': 404}))  # 请求非post
