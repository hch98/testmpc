from django.db import models
from users.models import User



class Type(models.Model):
    type_id = models.AutoField(verbose_name='类型id', max_length=4, primary_key=True)
    type_name = models.CharField(verbose_name='类型名称', max_length=10)

    def __str__(self):
        return self.type_name

    class Meta:
        db_table = 'tb_article_type'
        verbose_name_plural = verbose_name = '类型'


# 文章
class Article(models.Model):
    article_id = models.BigAutoField(verbose_name='文章编号', max_length=20, primary_key=True)
    title = models.CharField(verbose_name='标题', max_length=64)
    content = models.TextField(verbose_name='内容')
    simple_content = models.CharField(verbose_name='简介内容', max_length=128)
    page_view = models.PositiveIntegerField(verbose_name='阅读数', default=0)
    create_time = models.DateTimeField(verbose_name='发表时间', auto_now=True)
    flag = models.SmallIntegerField(verbose_name='0为草稿，1为发表,2为删除,3仅为新建的文章', default=0)  # 标志位
    type_id = models.IntegerField(verbose_name='类型id', db_index=True)
    user_id = models.ForeignKey(User, models.DO_NOTHING, db_column='user_id', db_index=True)

    def __unicode__(self):
        return self.article_id

    def __str__(self):
        return self.article_id

    class Meta:
        db_table = 'tb_article'
        ordering = ['create_time']  # 按时间排序
        index_together = ["flag", "create_time"]
        verbose_name_plural = verbose_name = '文章'


# 点赞
class Point(models.Model):
    point_id = models.AutoField(verbose_name='点赞编号', max_length=20, primary_key=True)
    point_count = models.IntegerField(verbose_name='点赞数', default=0)
    article_id = models.BigIntegerField(verbose_name='文章编号', db_index=True)

    class Meta:
        db_table = 'tb_article_point'
        verbose_name_plural = verbose_name = '点赞表'


# 用户点赞记录
class Record(models.Model):
    record_id = models.BigAutoField(verbose_name='用户点赞记录编号', primary_key=True)
    article_id = models.BigIntegerField(verbose_name='文章编号', db_index=True)
    flag = models.SmallIntegerField(verbose_name='0为没有点赞，1为已经点赞', default=1)
    user_id = models.ForeignKey(User, on_delete=models.DO_NOTHING, db_column='user_id', db_index=True)

    class Meta:
        db_table = 'tb_point_record'
        verbose_name_plural = verbose_name = '用户点赞记录表'


# 收藏
class Collection(models.Model):
    article_id = models.BigIntegerField(verbose_name='文章编号')
    user_id = models.IntegerField(verbose_name="用户ID")
    create_time = models.DateTimeField(verbose_name='收藏时间', auto_now=True, db_index=True)

    class Meta:
        db_table = 'tb_article_collection'
        unique_together = ('article_id', 'user_id')
        verbose_name_plural = verbose_name = '收藏'


# 评论
class Comment(models.Model):
    comment_id = models.BigAutoField(verbose_name='评论编号', max_length=20, primary_key=True)
    comment_content = models.CharField(verbose_name='评论内容', max_length=128)
    create_time = models.DateTimeField(verbose_name='评论时间', auto_now=True)
    article_id = models.BigIntegerField(verbose_name='文章编号')
    user_id = models.ForeignKey(User, models.DO_NOTHING, db_column='user_id', db_index=True)
    is_delete = models.SmallIntegerField(verbose_name='0为删除，1为有效', default=1)
    class Meta:
        db_table = 'tb_article_comment'
        ordering = ['create_time']  # 按时间排序
        index_together = ["article_id", "create_time"]
        verbose_name_plural = verbose_name = '评论'


# 回复
class Reply(models.Model):
    reply_id = models.BigAutoField(verbose_name='回复编号',max_length=20,primary_key=True)
    reply_content = models.CharField(verbose_name='回复内容',max_length=128)
    create_time = models.DateTimeField(auto_now=True,verbose_name='回复时间')
    comment_id = models.BigIntegerField(verbose_name='评论ID',db_index = True)
    target_id = models.BigIntegerField(verbose_name='0为回复了评论ID，其他的为回复id', default=0)
    to_user = models.ForeignKey(User, models.DO_NOTHING, related_name='to_user')
    from_user = models.ForeignKey(User, models.DO_NOTHING, related_name='from_user')
    is_delete = models.SmallIntegerField(verbose_name='0为删除，1为没有删除', default=1)

    class Meta:
        db_table = 'tb_reply'
        index_together = ["target_id", "create_time"]
        verbose_name_plural = verbose_name = '回复'


# 图片
class Photo(models.Model):
    photo_id = models.AutoField(verbose_name='图片编号', max_length=20, primary_key=True)
    photo_url = models.CharField(verbose_name='图片路径', max_length=64)
    create_time = models.DateTimeField(verbose_name='上传时间', auto_now=True)
    flag = models.SmallIntegerField(verbose_name='0为图片，1为视频', default=0)
    article_id = models.BigIntegerField(verbose_name='文章编号', db_index=True)

    class Meta:
        db_table = 'tb_article_photo'
        ordering = ['create_time']  # 按时间排序
        verbose_name_plural = verbose_name = '图片'
