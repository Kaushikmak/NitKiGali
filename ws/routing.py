from django.urls import re_path
from . import consumer

websocket_urlpatterns = [
    # Route for the matchmaking "waiting pool"
    re_path(r'ws/find_chat/$', consumer.MatchmakingConsumer.as_asgi()),
    
    # Route for the private chat rooms
    re_path(r'ws/chat/(?P<room_name>\w+)/$', consumer.ChatConsumer.as_asgi()),
]