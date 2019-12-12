# login用户登录，生成token
# 接收JSON数据
# user_account 用户输入用户名
# password 用户输入的密码
import json

from django.contrib.auth.hashers import check_password
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from users.forms import UserForm
from users.models import User

from users.utils import token_op


@csrf_exempt
def login(request):
    if request.method == "POST":
        login_req = json.loads (request.body)
        user_account = login_req['user_account']
        password = login_req['password']
        try:
            user = User.objects.get (user_account=user_account)
        except:
            return HttpResponse (json.dumps ({'code': '301'}))  # 用户不存在
        if check_password (password, user.password):
            # print ('数据库密码是：' + user.password)
            temp = user
            token = token_op.create_token (temp)
            return HttpResponse (
                json.dumps (
                    {
                        'code': '200',  # 成功状态码
                        'token': token,
                        'user_id': user.user_id,
                        'user_account': user.user_account,
                        'user_url': user.user_url,
                        'user_name': user.user_name,
                        'user_gender': user.user_gender,
                        'email': user.email,
                        'user_phone': user.user_phone,
                        'user_credit': user.user_credit,
                        'status': user.status,
                    }
                )
            )
        else:
            return HttpResponse (json.dumps ({'code': '302'}))  # 密码不正确
    else:
        return HttpResponse (json.dumps ({'code': '404'}))  # 请求非POST类型


# 用户登录，生成token
# 接收表单数据
# username 用户输入用户名
# password 用户输入的密码
# user 通过输入的用户名获取的数据库用户
@csrf_exempt
def login_demo(request):
    if request.method == "POST":
        login_form = UserForm (request.POST)  # 自定义登录表单
        if login_form.is_valid ():  # 确保用户名和密码都不为空
            username = login_form.cleaned_data['user_account']
            password = login_form.cleaned_data['password']
            try:
                user = User.objects.get (user_account=username)
            except:
                return HttpResponse (json.dumps ({'code': '301'}))  # 用户不存在
            if check_password (password, user.password):
                # print ('数据库密码是：' + user.password)
                temp = user
                token = token_op.create_token (temp)
                return HttpResponse (
                    json.dumps (
                        {
                            'code': '200',  # 成功状态码
                            'token': token,
                            'user_id': user.user_id,
                            'user_account': user.user_account,
                            'user_url': user.user_url,
                            'user_name': user.user_name,
                            'user_gender': user.user_gender,
                            'email': user.email,
                            'user_phone': user.user_phone,
                            'user_credit': user.user_credit,
                            'status': user.status,
                        }
                    )
                )
            else:
                return HttpResponse (json.dumps ({'code': '302'}))  # 密码不正确
        else:
            return HttpResponse (json.dumps ({'code': '402'}))  # 输入框未填完
    else:
        return HttpResponse (json.dumps ({'code': '404'}))  # 请求非POST类型
