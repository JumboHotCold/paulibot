"""
PauliBot URL Configuration
===========================
URL patterns for chatbot application endpoints.
"""

from django.urls import path
from . import views

urlpatterns = [
    # Frontend Pages
    path('', views.landing_view, name='landing'),
    path('chat/', views.chat_view, name='chat_view'),
    path('register/', views.register_page, name='register_page'),
    path('login/', views.login_page, name='login_page'),
    path('logout/', views.logout_page, name='logout_page'),

    # API Endpoints (AJAX)
    path('api/chat', views.chat_api, name='chat_api'),
    path('api/history', views.get_chat_history, name='history'), # Legacy support
    path('api/conversations', views.conversation_list, name='conversation_list'),
    path('api/conversations/<int:conversation_id>', views.conversation_detail, name='conversation_detail'),
    
    # API Auth (Optional/Legacy support)
    path('api/register', views.register_user, name='api_register'),
    path('api/login', views.login_user, name='api_login'),
]
