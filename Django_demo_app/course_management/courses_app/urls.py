"""URL's for courses_app."""
from django.urls import path

from courses_app import views

urlpatterns = [
    path('courses_page/', views.CourseView.as_view(), name='course_view'),
    path('admin_page/', views.AdminOnlyView.as_view(), name='admin_page'),
    path('add_course/', views.AddCourseView.as_view(), name='add_course'),
    path('enrolled_course/<int:pk>/',
         views.EnrolledCourseView.as_view(), name='enrolled_course'),
    path('delete_course/<int:pk>/', views.DeleteCourseView.as_view(),
         name='delete_course'),
]
