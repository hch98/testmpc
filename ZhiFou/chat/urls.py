# chat/urls.py
from django.urls import path

from . import views

urlpatterns = [
    # path('', views.index, name='index'),
    path('<str:from_id>-<str:to_id>/', views.room,name='room'),
    # path(r'^(?P<from_id>\d+)-(?P<to_id>\d+)/$', views.room),
]