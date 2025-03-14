"""Views for course access with user authentication in the courses app."""

from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def course_view(request):
    """Render the course page for authenticated users.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: A response with a welcome message.
    """
    return render(request, 'courses_app/courses_page.html',
                  {'message': 'This is the Courses page'})


def no_permission_view(request):
    """Render a message for users who are not authenticated.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: A response with a permission denial message.
    """
    return render(request, 'courses_app/no_permissions_page.html',
                  {'message': 'You have no permissions to view this page'})
