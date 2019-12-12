from django.urls import path

from article.service import DraftBox, QueryArticle, UploadPhoto, UploadArticle


urlpatterns = {
    # 查询文章
    path('queryArticle', QueryArticle.queryArticle),  # 首页查询
    #path('readFullArticle', UploadArticle.readFullArticle),  # 阅读全文
    path('queryArticleByTypeId', QueryArticle.queryArticleByTypeId),  # 分类查询
    path('queryArticleDetailed', QueryArticle.queryArticleDetailed),
    path('queryArticleByMyself', QueryArticle.queryArticleByMyself),
    path('queryCollectionByUserId', QueryArticle.queryCollectionByUserId),
    path('updatePageView', QueryArticle.updatePageView),

    # 上传图片或者视频
    path('uploadPhoto', UploadPhoto.uploadPhoto),

    # 上传文章删除文章
    path('createArticleId', UploadArticle.createArticleId),   # 生成文章ID
    path('delArticleOrDraft', UploadArticle.delArticleOrDraft),   # 删除文章或者草稿
    path('saveArticle', UploadArticle.saveArticle),  # 保存文章（发表文章或者保存草稿）


    path('queryDraftBox', DraftBox.queryDraftBox),  # 查看草稿箱信息
    path('editorDraftBox', DraftBox.editorDraftBox),  # 编辑草稿箱信息
}
