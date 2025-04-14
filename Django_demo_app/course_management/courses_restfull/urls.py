"""URLs for courses_restfull."""
from django.urls import path

from courses_restfull.views import LoginView, ProtectedView, RefreshTokenView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('refresh/', RefreshTokenView.as_view(), name='refresh'),
    path('protected/', ProtectedView.as_view(), name='protected'),
]
