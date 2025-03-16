"""This file is used to create custom template tags."""
from datetime import datetime

from django import template

register = template.Library()


@register.simple_tag
def get_current_time():
    """Return the current time.

    Returns:
        str: The current time in the format '%d-%m-%Y %H:%M:%S'.
    """
    return datetime.now().strftime('%d-%m-%Y %H:%M:%S')


@register.filter
def join_strings(value1, value2):
    """Join two strings with a space.

    Args:
        value1 (str): The first string.
        value2 (str): The second string.

    Returns:
        str: The two strings joined with a space.
    """
    return f'{value1} {value2}'


@register.inclusion_tag('accounts/user_info.html')
def show_user_info(user):
    """Include user info template.

    Args:
        user (User): The user to display info for.

    Returns:
        dict: The user info to display in the template.
    """
    return {'user': user}
