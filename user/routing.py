from django.urls import re_path, path

from . import consumers

websocket_urlpatterns = [ 
    path(r"dm/<str:dm>", consumers.ChatConsumer.as_asgi()),
]
