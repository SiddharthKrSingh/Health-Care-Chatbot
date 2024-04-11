# urls.py
from django.urls import path
from .views import chat_view

urlpatterns = [
    path('chat/', chat_view, name='chat'),
    # Add other URL patterns as needed
]
