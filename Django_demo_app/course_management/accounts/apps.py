"""This file is used to configure the app name"""
from django.apps import AppConfig


class AccountsConfig(AppConfig):
    """Configuration class for the accounts Django application."""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'
