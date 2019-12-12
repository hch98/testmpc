from django import forms
from captcha.fields import CaptchaField

# 登录表
from django.core.exceptions import ValidationError

from .models import User


# 登录表
class UserForm (forms.Form):
    user_account = forms.CharField (label="用户名", max_length=128, widget=forms.TextInput (attrs={'class': 'form-control'}))
    password = forms.CharField (label="密码", max_length=256,
                                widget=forms.PasswordInput (attrs={'class': 'form-control'}))
    # captcha = CaptchaField (label='验证码')  # 图片验证码+输入框


# # 定义验证器
# def user_account_validate(user_account):
#     u = User.objects.filter (user_account=user_account)
#     if len (u):
#         raise ValidationError ('用户名已存在')


# 注册表
class RegisterForm (forms.Form):
    user_account = forms.CharField (label="用户账号", max_length=25, required=True)
    user_name = forms.CharField (label="用户名", max_length=11, required=True)
    # user_phone = forms.CharField (label="手机号", max_length=11, required=True)
    # email = forms.EmailField (label="邮箱", required=True)
    password = forms.CharField (label="密码", min_length=6, max_length=128, required=True)
    # user_gender = forms.ChoiceField (
    #     label="性别", choices=((0, "female"), (1, "male"),), required=True
    # )
    # confirm_password = forms.CharField(widget=forms.PasswordInput(
    #     attrs={'class': 'form-control', 'placeholder': '确认密码', 'required': True}))
