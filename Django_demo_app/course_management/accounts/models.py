"""This file is used to create custom user model. """
from django.contrib.auth.models import (
    AbstractUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from django.utils import timezone


class CustomUserManager(BaseUserManager):
    """Custom user model manager for User model."""

    def create_user(self, email, phone_number, password=None, **extra_fields):
        """Create and return a new user.

        Args:
            email (str): The email address of the user.
            phone_number (str): The phone number of the user.
            password (str): The password of the user.
            **extra_fields: Additional fields to create the user with.

        Returns:
            User: The newly created user.
        """
        if not email:
            raise ValueError('The Email field must be set')
        if not phone_number:
            raise ValueError('The Phone number field must be set')
        email = self.normalize_email(email)
        user = self.model(
            email=email, phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(
            self, email, phone_number, password=None, **extra_fields):
        """Create and return a new superuser.

        Args:
            email (str): The email address of the user.
            phone_number (str): The phone number of the user.
            password (str): The password of the user.
            **extra_fields: Additional fields to create the user with.

        Returns:
            User: The newly created superuser.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, phone_number, password, **extra_fields)

    def active_users_after_date(self, date):
        """Return all users who joined after the given date.

        Args:
            date (datetime): The date to filter users by.

        Returns:
            QuerySet: A queryset of users who joined after the given date.
        """
        return self.filter(is_active=True, date_joined__gte=date)


class CustomUser(AbstractUser, PermissionsMixin):
    """Custom user model for the application."""
    email = models.EmailField(unique=True, verbose_name='Email address')
    phone_number = models.CharField(
        max_length=15, unique=True, verbose_name='Phone number')
    first_name = models.CharField(
        max_length=30, blank=True, verbose_name='First name')
    last_name = models.CharField(
        max_length=50, blank=True, verbose_name='Last name')
    date_of_birth = models.DateField(
        null=True, blank=True, verbose_name='Date of birth')
    profile_picture = models.ImageField(
        upload_to='profile_pictures/', null=True, blank=True,
        verbose_name='Profile picture')
    date_joined = models.DateTimeField(
        default=timezone.now, verbose_name='Date joined')
    is_active = models.BooleanField(default=True, verbose_name='Active')
    is_staff = models.BooleanField(default=False, verbose_name='Staff')
    preferred_language = models.CharField(
        max_length=10, choices=[
            ('en', 'English'),
            ('uk', 'Ukrainian'),
        ], default='en', verbose_name='Preferred language')

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number']

    class Meta:
        """Meta options for the CustomUser model."""
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        permissions = [
            ('can_view_profiles', 'Can view user profiles'),
            ('can_edit_profiles', 'Can edit user profiles'),
        ]

    def __str__(self):
        """Return the string representation of the user.

        Returns:
            str: The string representation of the user.
        """
        return self.email

    @property
    def full_name(self):
        """Return the full name of the user.

        Returns:
            str: The full name of the user.
        """
        return f'{self.first_name} {self.last_name}'.strip()
