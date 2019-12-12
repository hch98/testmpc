

def queryDraftBox():
    sql = 'select t1.*,p2.photo_url,p2.photo_flag \
            from ( \
            select a.article_id,a.title,a.simple_content,a.page_view,a.create_time,t.type_name,t.type_id \
            from tb_article a,tb_article_type t \
            where a.user_id=1001 and a.flag = 0 and a.type_id = t.type_id ) t1 \
            left join (select a.article_id,ph.photo_url,ph.flag as photo_flag \
            from tb_article_photo ph,tb_article a \
            where a.article_id=ph.article_id \
            group by a.article_id ) p2 \
            on t1.article_id = p2.article_id order by t1.create_time desc LIMIT %s,10'
    return sql

