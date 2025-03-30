"""Mixins for the courses app."""
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect

from .models import Course


# 1. LoginRequiredMixin (Inherits from Django's built-in LoginRequiredMixin)
class LoginRequiredMixin:
    """Ensure that the user is logged in before accessing the view."""

    def dispatch(self, request, *args, **kwargs):
        """Check if the user is authenticated.

        Args:
            request (HttpRequest): The HTTP request object.
            args: Additional positional arguments.
            kwargs: Additional keyword arguments.

        Returns:
            HttpResponse: The response from the view.
        """
        if not request.user.is_authenticated:
            messages.error(
                request, 'You must be logged in to access this page.')
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)


# 2. AdminRequiredMixin
class AdminRequiredMixin:
    """Ensure that only admin users can access the view."""

    def dispatch(self, request, *args, **kwargs):
        """Check if the user is an admin.

        Args:
            request (HttpRequest): The HTTP request object.
            args: Additional positional arguments.
            kwargs: Additional keyword arguments.

        Raises:
            Http404: If the user is not an admin.

        Returns:
            HttpResponse: The response from the view.
        """
        if not request.user.is_staff:
            raise Http404('You do not have permission to view this page.')
        return super().dispatch(request, *args, **kwargs)


# 3. LoggingMixin
class LoggingMixin:
    """Log when a view is accessed."""

    def dispatch(self, request, *args, **kwargs):
        """Log the user accessing the view.

        Args:
            request (HttpRequest): The HTTP request object.
            args: Additional positional arguments.
            kwargs: Additional keyword arguments.

        Returns:
            HttpResponse: The response from the view.
        """
        print(
            f'User: {request.user.username} is accessing the '
            f'{self.__class__.__name__} view.')
        return super().dispatch(request, *args, **kwargs)


# 4. OwnerRequiredMixin
class OwnerRequiredMixin:
    """Ensure the user is the owner of the object being accessed."""

    model = None

    def dispatch(self, request, *args, **kwargs):
        """Check if the user is the owner of the object.

        Args:
            request (HttpRequest): The HTTP request object.
            args: Additional positional arguments.
            kwargs: Additional keyword arguments.

        Raises:
            Http404: If the user is not the owner of the object.

        Returns:
            HttpResponse: The response from the view.
        """
        obj = self.get_object()
        if obj.created_by != request.user:
            raise Http404('You are not authorized to access this object.')
        return super().dispatch(request, *args, **kwargs)


# 5. ObjectExistsMixin
class ObjectExistsMixin:
    """Ensure that an object exists before performing an action."""

    model = None

    def dispatch(self, request, *args, **kwargs):
        """Check if the object exists.

        Args:
            request (HttpRequest): The HTTP request object.
            args: Additional positional arguments.
            kwargs: Additional keyword arguments.

        Raises:
            Http404: If the object does not exist.

        Returns:
            HttpResponse: The response from the view.
        """
        obj = self.get_object_or_404(self.model, pk=kwargs['pk'])
        if not obj:
            raise Http404('Object does not exist.')
        return super().dispatch(request, *args, **kwargs)


# 6. FormSuccessMessageMixin
class FormSuccessMessageMixin:
    """Display a success message upon form submission."""

    success_message = 'Form submitted successfully!'

    def form_valid(self, form):
        """Handle the form submission and display a success message.

        Args:
            form (Form): The form being submitted.

        Returns:
            HttpResponse: The response from the view.
        """
        messages.success(self.request, self.success_message)
        return super().form_valid(form)


# 7. PaginationMixin
class PaginationMixin:
    """Handle pagination in views."""

    paginate_by = 10

    def get_paginated_queryset(self, queryset):
        """Paginate the queryset based on the paginate_by attribute.

        Args:
            queryset (QuerySet): The queryset to paginate.

        Returns:
            Page: The paginated queryset.
        """
        paginator = Paginator(queryset, self.paginate_by)
        page_number = self.request.GET.get('page')
        return paginator.get_page(page_number)


# 8. SearchMixin
class SearchMixin:
    """Allow filtering or searching of a queryset based on GET parameters."""

    search_fields = []

    def get_search_query(self):
        """Get the search query from GET parameters.

        Returns:
            str: The search query string.
        """
        query = self.request.GET.get('search', '')
        return query

    def get_queryset(self):
        """Get the filtered queryset based on the search query.

        Returns:
            QuerySet: The filtered queryset.
        """
        queryset = super().get_queryset()
        query = self.get_search_query()
        if query:
            filters = {
                f'{field}__icontains': query for field in self.search_fields}
            queryset = queryset.filter(**filters)
        return queryset


# 9. EnrollmentCheckMixin
class EnrollmentCheckMixin:
    """Ensure a user is enrolled in the course before allowing access."""

    model = None

    def dispatch(self, request, *args, **kwargs):
        """Check if the user is enrolled in the course.

        Args:
            request (HttpRequest): The HTTP request object.
            args: Additional positional arguments.
            kwargs: Additional keyword arguments.

        Returns:
            HttpResponse: The response from the view.
        """
        user = request.user
        course = get_object_or_404(self.model, pk=kwargs['pk'])
        if not course.enrollment_set.filter(user=user).exists():
            course.enrollment_set.create(user=user)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """Add course to the context.

        Args:
            kwargs: Additional keyword arguments.

        Returns:
            dict: Context data for the template.
        """
        context = super().get_context_data(**kwargs)
        course = get_object_or_404(Course, pk=kwargs['pk'])
        context['course'] = course
        return context


# 10. CourseExistsMixin
class CourseExistsMixin:
    """Check if a course exists in the system."""

    def dispatch(self, request, *args, **kwargs):
        """Check if the course exists.

        Args:
            request (HttpRequest): The HTTP request object.
            args: Additional positional arguments.
            kwargs: Additional keyword arguments.

        Raises:
            Http404: If the course does not exist.

        Returns:
            HttpResponse: The response from the view.
        """
        try:
            self.course = Course.objects.get(pk=kwargs['pk'])
        except Course.DoesNotExist as exc:
            raise Http404('Course not found.') from exc
        return super().dispatch(request, *args, **kwargs)
