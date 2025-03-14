"""URLs for members_app."""
from django.urls import path
from members_app import views

urlpatterns = [
    path('session/', views.session_view, name='session_view'),
]
