from django.urls import path

from comment.service import Comment

urlpatterns = {
    path('queryComment', Comment.queryComment),
    path('deleteComment', Comment.deleteComment),
    path('addComment', Comment.addComment),

}
