import json
import time
import hashlib  # 涉及安全散列和消息摘要，提供多个不同的加密算法接口，eg：sha256，md5……
from django.core import signing  # django内置模块，加密解密任何数据
from django.core.cache import cache
from django.http import HttpResponse

# version 2：使用signing
HEADER = {'typ': 'JWT', 'alg': 'default'}
KEY = 'ZhiFou'
SALT = 'django.core.signing'
TIME_OUT = 30 * 60  # 过期时间 30min


def encrypt(obj):
    """加密"""
    value = signing.dumps (obj, key=KEY, salt=SALT)
    value = signing.b64_encode (value.encode ()).decode ()
    return value


def decrypt(obj):
    """解密"""
    src = signing.b64_decode (obj.encode ()).decode ()
    raw = signing.loads (src, key=KEY, salt=SALT)
    print ('类型：', type (raw))
    return raw


def create_token(user):
    """生成token信息"""
    # 1. 加密头信息
    header = encrypt (HEADER)
    # 2. 构造Payload:用户id+用户名+密码+发行时间
    payload = {"id": user.user_id, "username": user.user_account, "password": user.password, "iat": time.time ()}
    payload = encrypt (payload)
    # 3. 生成签名
    # md5 = hashlib.md5 ()
    # md5.update (("%s.%s" % (header, payload)).encode ())
    # signature = md5.hexdigest ()
    # token = "%s.%s.%s" % (header, payload, signature)  # 用.分割三部分
    token = packing_token(header, payload)
    # 存储到缓存中
    cache.set (user.user_id, token, TIME_OUT)
    return token


def packing_token(header, payload):
    # 3. 生成签名
    md5 = hashlib.md5 ()
    md5.update (("%s.%s" % (header, payload)).encode ())
    signature = md5.hexdigest ()
    token = "%s.%s.%s" % (header, payload, signature)  # 用.分割三部分
    return token

# 获取token的信息主体
def get_payload(token):
    payload = str (token).split ('.')[1]
    payload = decrypt (payload)
    return payload


# 通过token获取用户名
def get_username(token):
    payload = get_payload (token)
    return payload['username']
    pass


# 验证token，通过用户id
def check_token(token):
    # username = get_username (token)
    # last_token = cache.get (username)
    try:
        user_id = get_userid(token)
    except: # 无法解析的token
        print('token无法解析')
        return False
    last_token = cache.get(user_id)
    if last_token:  # 用户存在token
        return last_token == token  # 比较传来的和redis内的
    return False    # 用户不存在token


# 通过token获取用户id
def get_userid(token):
    payload = get_payload (token)
    return payload['id']


# 通过token获取用户密码
def get_password(token):
    payload = get_payload (token)
    return payload['password']


# 装饰器，验证token
# （1）check_token:解析token，获取token包装信息的user_id，并比较此token和id对应redis的token是否相同
# （2）校验传入的user_id和token包装信息user_id是否一致,防止盗用token
def checkToken(param):
    def __checkToken(func):
        def warpper(request):
            try:
                json_req = json.loads(request.body)
                token = json_req['token']
                user_id = json_req['user_id']
            except:
                return HttpResponse (json.dumps ({'code': '4401'}))  # 获取不到参数token/user_id
            if check_token(token):  # 验证token
                if get_userid(token) == user_id:
                    return func (request)   # 验证通过，继续执行后续
                else:
                    return HttpResponse (json.dumps ({'code': '4402'}))  # 实际用户id与token的id不匹配
            else:
                return HttpResponse (json.dumps ({'code': '4403'}))  # token无法解析/验证失败
        return warpper
    return __checkToken


# 忘记密码，邮件找回的token
def create_email_token(user):
    """生成token信息"""
    # 1. 加密头信息
    header = encrypt (HEADER)
    # 2. 构造Payload:用户id+用户名+密码+发行时间
    payload = {"id": user.user_id, "email":user.email, "iat": time.time ()}
    payload = encrypt (payload)
    # 3.生成签名并返回token
    token = packing_token(header, payload)
    # 存储到缓存中
    cache.set (user.email, token, TIME_OUT)
    return token