"""App configuration for the courses_app application."""
from django.apps import AppConfig


class CoursesAppConfig(AppConfig):
    """Configuration class for the courses_app Django application."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'courses_app'
