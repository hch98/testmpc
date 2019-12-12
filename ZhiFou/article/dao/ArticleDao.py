
'''
    数据层存放SQL
'''


# 首页文章查询
from django_redis import get_redis_connection

from article.models import Point, Photo, Type, Comment


def queryArticle(order):
    sql = 'select t1.*,p2.photo_url,p2.photo_flag,IFNULL(p3.comment_count,0) as comment_count from \
               (select a.article_id,a.title,a.simple_content,a.page_view,a.create_time, \
               u.user_url,u.user_name,u.user_account,t.type_name,t.type_id,r.flag AS point_flag,p.point_count\
               from tb_article a LEFT JOIN (SELECT * from tb_point_record WHERE user_id = %s ) r \
               on a.article_id=r.article_id,tb_user u,tb_article_type t,tb_article_point p \
               where a.user_id = u.user_id \
               and a.type_id = t.type_id \
               and a.flag = 1 \
               and a.article_id = p.article_id ) t1 \
               left join ( \
               select a.article_id,ph.photo_url,ph.flag as photo_flag from tb_article_photo ph,tb_article a \
               where a.article_id=ph.article_id  group by a.article_id \
               ) p2 on t1.article_id = p2.article_id \
               left join (select count(c.article_id) as comment_count,c.article_id \
               from tb_article_comment c,tb_article a where c.article_id = a.article_id group by c.article_id) \
               p3 on t1.article_id = p3.article_id ' + order + ' LIMIT %s,10'
    return sql


def queryArticleByTypeId(order):
    sql = 'select t1.*,p2.photo_url,IFNULL(p3.comment_count,0) as comment_count from (select a.article_id,a.title,a.simple_content,a.page_view,a.create_time,  \
                u.user_url,u.user_name,u.user_account,r.flag AS point_flag,p.point_count  \
                from tb_article a LEFT JOIN (SELECT * from tb_point_record WHERE user_id = %s ) r on a.article_id=r.article_id,tb_user u,tb_article_type t,tb_article_point p  \
                where a.user_id = u.user_id  \
                and a.type_id = t.type_id  \
                and a.flag = 1  \
                and a.type_id = %s  \
                and a.article_id = p.article_id ) t1  \
                left join (select a.article_id,ph.photo_url from tb_article_photo ph,tb_article a where ph.flag = 0 and a.article_id=ph.article_id group by a.article_id) p2 \
                on t1.article_id = p2.article_id  \
                left join (select count(c.article_id) as comment_count,c.article_id from tb_article_comment c,tb_article a where c.article_id = a.article_id group by c.article_id)  \
                p3 on t1.article_id = p3.article_id ' + order + ' LIMIT %s,10'
    return sql



# 查看文章详情
def queryArticleDetailed():
    sql = ' select a.article_id,a.title,a.content,a.create_time,u.user_id, \
            u.user_url,user_name,u.user_account,p.point_count,t.type_id,t.type_name,r.flag as point_flag \
            from tb_article a  \
            left join (SELECT * from tb_point_record WHERE user_id =%s) r  \
            on a.article_id=r.article_id,tb_user u,tb_article_point p,tb_article_type t \
            where a.user_id = u.user_id  \
            and a.type_id = t.type_id \
            and a.flag = 1  \
            and a.article_id = %s  \
            and a.article_id = p.article_id '
    return sql


def queryCollectionByUserId():
    sql = 'select t1.*,p2.photo_url,p2.photo_flag,IFNULL(p3.comment_count,0) as comment_count  from ( \
                    select a.article_id,a.title,a.simple_content,a.page_view,a.create_time,p.point_count,t.type_name,t.type_id \
                    from tb_article_collection c,tb_article a,tb_article_point p,tb_article_type t \
                    where c.user_id = %s \
                    and a.article_id = c.article_id\
                    and a.flag = 1 \
                    and a.article_id = p.article_id \
                    and a.type_id = t.type_id ) t1 \
                    left join ( \
                    select a.article_id,ph.photo_url,ph.flag as photo_flag from tb_article_photo ph,tb_article a \
                    where a.article_id=ph.article_id  \
                    group by a.article_id ) p2 \
                    on t1.article_id = p2.article_id \
                    left join ( \
                    select count(c.article_id) as comment_count,c.article_id \
                    from tb_article_comment c,tb_article a \
                    where c.article_id = a.article_id \
                    group by c.article_id) p3 \
                    on t1.article_id = p3.article_id order by t1.create_time desc '+' LIMIT %s,10'
    return sql



#by huangcaihuan 12.12

#批量获取文章点赞数量的接口
def queryPointCount(articles):
    point=Point.objects.filter(article_id__in=articles).values("point_count")
    return list(point)


#批量获取文章图片信息的接口
def queryPhotoInfo(articles):
    photo = Photo.objects.filter(article_id__in=articles).values("photo_url","flag")
    return photo



# 返回文章类型名称，放进redis存着
def queryTypeName(type_id):
    try:
        conn = get_redis_connection('default')
        # 先获取key是否存在
        type_name = conn.hget('type_name', type_id)
        # redis不存在该类型的名称,则查询数据库数据，然后放进redis
        if type_name is None:
            type = Type.objects.get(type_id=type_id)
            type_name=type.type_name
            conn.hset('type_name', type_id,type_name)
        else:
            type_name=type_name.decode('utf-8')
    except:
        return "发生异常"
    return type_name