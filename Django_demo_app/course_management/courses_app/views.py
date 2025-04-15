"""Views for course access with user authentication in the courses app."""
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import DeleteView, TemplateView

from .forms import CourseForm
from .mixins import AdminRequiredMixin, EnrollmentCheckMixin, LoggingMixin
from .models import Course


class CourseView(LoggingMixin, TemplateView):
    """View for displaying the courses page."""

    template_name = 'courses_app/courses_page.html'

    def get_context_data(self, **kwargs):
        """Context data to the template.

        Args:
            kwargs: Additional keyword arguments.

        Returns:
            dict: Context data for the template.
        """
        context = super().get_context_data(**kwargs)
        context['message'] = 'This is the Courses page'
        context['courses'] = Course.objects.all()
        return context


class AdminOnlyView(AdminRequiredMixin, TemplateView):
    """View for admin users only."""

    template_name = 'courses_app/admin_page.html'


class AddCourseView(AdminRequiredMixin, TemplateView):
    """View for adding a new course."""

    template_name = 'courses_app/add_course.html'

    def get(self, request, *args, **kwargs):
        """Handle GET request and render the form.

        Args:
            request (HttpRequest): The HTTP request object.
            args: Additional positional arguments.
            kwargs: Additional keyword arguments.

        Returns:
            HttpResponse: The response with the course form.
        """
        form = CourseForm()
        return self.render_to_response({'form': form, 'request': request})

    def post(self, request, *args, **kwargs):
        """Handle POST request to save the course.

        Args:
            request (HttpRequest): The HTTP request object.
            args: Additional positional arguments.
            kwargs: Additional keyword arguments.

        Returns:
            HttpResponse: The response from the view.
        """
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.created_by = request.user
            course.save()
            return redirect('course_view')
        return self.render_to_response({'form': form})


class EnrolledCourseView(EnrollmentCheckMixin, TemplateView):
    """View for showing a course that the user is enrolled in."""

    template_name = 'courses_app/enrolled_course.html'
    model = Course


class DeleteCourseView(DeleteView):
    """View for deleting a course."""

    model = Course
    template_name = 'courses_app/course_confirm_delete.html'
    success_url = reverse_lazy('course_view')


class HomeView(TemplateView):
    """View for the home page."""

    template_name = 'courses_app/home.html'
