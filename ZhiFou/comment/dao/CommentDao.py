from article.models import Comment


def queryComment():
    sql = 'select c.comment_id,c.comment_content,c.create_time,u.user_id,u.user_name,u.user_url \
                    from tb_article_comment c, tb_user u where c.is_delete = 1 and c.user_id = u.user_id and c.article_id = %s \
                    order by create_time desc'+' LIMIT %s,10'
    return sql




#Vsersion 12.12 huangcaihuan

#批量获取文章评论数量的接口
def queryComentCount(articles):
    json_list=[]
    for i in articles:
        comment = Comment.objects.filter(article_id=i).count()
        dic={ "comment_count":comment}
        json_list.append(dic)
    return json_list