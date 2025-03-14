"""Views for handling user input and session data in the members app."""

from django.shortcuts import render


def session_view(request):
    """Demonstrate the usage of request.session to store and retrieve data.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: A response object that renders the session data page.
    """
    if request.method == 'POST':
        user_input = request.POST.get('user_input')
        if 'user_inputs' not in request.session:
            request.session['user_inputs'] = []

        request.session['user_inputs'].insert(0, user_input)

        request.session.modified = True

    user_inputs = request.session.get('user_inputs', [])

    return render(request, 'members_app/session.html',
                  {'user_inputs': user_inputs})
