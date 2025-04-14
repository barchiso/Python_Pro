"""Views for the courses RESTful API."""
import jwt
from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from courses_restfull.authentication import CustomJWTAuthentication
from courses_restfull.utils import (generate_access_token,
                                    generate_refresh_token)

User = get_user_model()


class LoginView(APIView):
    """Login view for obtaining JWT tokens."""

    authentication_classes = []
    permission_classes = []

    def post(self, request):
        """Handle user login and return JWT tokens.

        Args:
            request: The HTTP request object.

        Returns:
            Response: A JSON response with access and refresh tokens.
        """

        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(username=email, password=password)

        if not user:
            return Response({'error': 'Wrong username or password.'},
                            status=status.HTTP_401_UNAUTHORIZED,
                            )

        access_token = generate_access_token(user)
        refresh_token = generate_refresh_token(user)

        return Response({'access': access_token, 'refresh': refresh_token})


class RefreshTokenView(APIView):
    """View for refreshing JWT access tokens."""

    authentication_classes = []
    permission_classes = []

    def post(self, request):
        """Handle token refresh and return new access token.

        Args:   
            request: The HTTP request object.

        Returns:
            Response: A JSON response with the new access token.
            """
        refresh_token = request.data.get('refresh')
        try:
            payload = jwt.decode(
                refresh_token, settings.JWT_SECRET_KEY, algorithms=['HS256'])
            user_id = payload['user_id']
        except jwt.ExpiredSignatureError:
            return Response({'error': 'Refresh token has expired.'},
                            status=status.HTTP_401_UNAUTHORIZED,
                            )
        except jwt.InvalidTokenError:
            return Response({'error': 'Invalid refresh token!'},
                            status=status.HTTP_400_BAD_REQUEST,
                            )

        user = User.objects.get(id=user_id)
        access_token = generate_access_token(user)
        return Response({'access': access_token})


class ProtectedView(APIView):
    """Protected view requiring JWT authentication."""

    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Handle GET request for protected view.

        Args:
            request: The HTTP request object.

        Returns:
            Response: A JSON response with a message.
        """
        return Response({
            'message': f'Hello, {request.user.username}! Access granted.'
        })
