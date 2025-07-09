from django.urls import re_path
from .consumers import CallConsumer


websocket_urlpatterns = [
    re_path(r'ws/room/(?P<code>\w+)/$', CallConsumer.as_asgi(), name='call-room'),
]