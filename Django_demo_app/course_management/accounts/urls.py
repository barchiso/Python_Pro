"""URL's for account."""
from django.urls import path

from accounts import views

urlpatterns = [
    path('tags/', views.tags_page, name='tags_page'),
    path('user_info/', views.user_info_page, name='user_info_page'),
]
