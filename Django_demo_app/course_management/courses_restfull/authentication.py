"""Custom JWT Authentication for Django REST Framework."""
from datetime import datetime, timezone

import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils import timezone as dj_timezone
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

User = get_user_model()


class CustomJWTAuthentication(BaseAuthentication):
    """Custom JWT Authentication class for Django REST Framework."""

    def authenticate(self, request):
        """Authenticate the user using JWT token.

        Args:
            request: The HTTP request object.

        Returns:
            tuple: A tuple containing the user and the token.
            None: If authentication fails.

        Exceptions:
            AuthenticationFailed: If the token is invalid or expired.

        Raises:
            AuthenticationFailed: If the token is missing or invalid.
        """
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):

            return None

        token = auth_header.split(' ')[1]

        try:
            payload = jwt.decode(
                token, settings.JWT_SECRET_KEY, algorithms=['HS256'])
            user_id = payload.get('user_id')
            exp = payload.get('exp')

            if user_id is None or exp is None:
                raise AuthenticationFailed(
                    'Token payload missing required fields')

            if datetime.fromtimestamp(exp,
                                      tz=timezone.utc,
                                      ) < dj_timezone.now():
                raise AuthenticationFailed('Token is expired')

            user = User.objects.get(id=user_id)

            return (user, token)

        except User.DoesNotExist as e:
            raise AuthenticationFailed('User not found') from e
        except jwt.ExpiredSignatureError as e:
            raise AuthenticationFailed('Token has expired') from e
        except jwt.InvalidTokenError as e:
            raise AuthenticationFailed('Invalid token') from e
