from django.urls import path
from .views import init_chat, chat_room

urlpatterns = [
    path('init/<int:user_id>/', init_chat, name='init_chat'),
    path('room/<int:convo_id>/', chat_room, name='chat_room'),
]