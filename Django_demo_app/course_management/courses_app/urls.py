"""URL's for courses_app."""
from django.urls import path

from courses_app import views

urlpatterns = [
    path('courses_page/', views.course_view, name='course_view'),
]
