"""Utility functions for generating JWT tokens."""
from datetime import timedelta

import jwt
from django.conf import settings
from django.utils import timezone


def generate_access_token(user):
    """Generate a JWT access token for the user."""
    lifetime = getattr(settings, 'JWT_ACCESS_TOKEN_LIFETIME', 300)
    payload = {
        'user_id': user.id,
        'exp': timezone.now() + timedelta(seconds=lifetime),
        'iat': timezone.now()
    }
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm='HS256')


def generate_refresh_token(user):
    """Generate a JWT refresh token for the user."""
    payload = {
        'user_id': user.id,
        'exp': timezone.now() + timedelta(days=7),
        'iat': timezone.now()
    }
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm='HS256')
