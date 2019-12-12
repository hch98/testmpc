# chat/routing.py
from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<from_id>\d+)-(?P<to_id>\d+)/$', consumers.ChatConsumer),
]