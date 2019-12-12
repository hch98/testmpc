from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


# UserManager
# UserManager是User的管理类
# 由该类创建User
# 创建一个User只需要调用User.objects.create_user
class UserManager (BaseUserManager):
    def create_user(self, user_account,user_name, password, user_phone='', email='', user_gender=0, user_url='', user_credit=0,
                    status=1):
        user = self.model (
            user_account=user_account,
            email=email, user_name=user_name,
            user_url=user_url, user_gender=user_gender, user_credit=user_credit, user_phone=user_phone,
            status=status,
        )

        user.set_password (password)
        user.save (using=self._db)
        return user


class User (AbstractBaseUser):
    user_id = models.AutoField (verbose_name="用户ID", max_length=8, primary_key=True,db_column='user_id')
    user_account = models.CharField (verbose_name="账号", max_length=25, unique=True, db_index=True)
    user_name = models.CharField (verbose_name="用户名", max_length=25)
    email = models.EmailField (verbose_name="邮箱", max_length=20, unique=False, db_index=True)
    GENDER_IN_CHOICES = ((0, 'female'), (1, 'male'))
    user_url = models.CharField (verbose_name="头像", max_length=64)
    user_gender = models.SmallIntegerField (verbose_name="性别", choices=GENDER_IN_CHOICES, default=0)
    user_phone = models.CharField (verbose_name="手机号", max_length=11)
    user_credit = models.IntegerField (verbose_name="用户积分", default=0)
    status = models.SmallIntegerField (verbose_name="状态(1为账户存在，0为不存在)", default=1)

    #last_login为django自带字段，赋空值避免迁移数据库出现该字段
    last_login = ''

    objects = UserManager ()

    #设置django作为账号的字段
    USERNAME_FIELD = "user_account"

    #设置django必须的字段
    # REQUIRED_FIELDS = ["user_gender", "email"]

    def __str__(self):
        return self.user_account

    class Meta:
        db_table = 'tb_user'
