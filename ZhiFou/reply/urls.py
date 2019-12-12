from django.urls import path

from reply import views

urlpatterns = {
    path('addReplyToComment', views.addReplyToComment),
    path('addReplyToReply', views.addReplyToReply),
    path('deleteReply', views.deleteReply),
    path('queryReply', views.queryReply),
}