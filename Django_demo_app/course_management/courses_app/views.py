"""Views for course access with user authentication in the courses app."""
from django.shortcuts import render


def course_view(request):
    """Render the course page for authenticated users.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: A response with a welcome message.
    """
    message = ('This is the Courses page'
               if request.user.is_authenticated
               else 'You have no permissions to view this page'
               )
    return render(
        request, 'courses_app/courses_page.html', {'message': message})
