"""Views for the accounts app."""
from django.shortcuts import render


def tags_page(request):
    """Render the tags page.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The response object
    """
    return render(request, 'accounts/tags.html')


def user_info_page(request):
    """Render the user info page.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The response object
    """
    return render(request, 'accounts/user_info.html')

