#import users

from django.urls import path, include
from users.view import loginView, passwdView, emailView

from users import views
from users.view import loginView

urlpatterns = [
    path('info/<str:user_id>',views.view_UserInfo),
    path('update',views.update_UserInfo),
    path('image',views.demo_image),
    path('profile/<str:url>',views.get_profile_photo),
    path('uploadfiles',views.upload_files),
    path ('captcha', include ('captcha.urls')),  # 验证码
    path ('login_demo', loginView.login_demo),        # 表单类型登录
    path ('login', loginView.login),        # json数据登录
    path ('reg', views.register_User),
    # path ('reg_demo', views.register_User2),
    path ('viewDemo', views.viewDemo),
    path('resetpasswd', passwdView.reset_password),     # 登录状态下修改密码
    path ('forgetpasswd', emailView.send_email_reset_password),  # 邮件链接重置密码
    path ('changepasswd/<str:token>', passwdView.reset_password_by_email)  # 发送邮件找回密码
]