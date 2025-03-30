"""Django models for the courses app."""
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Course(models.Model):
    """Model representing a course."""

    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='courses_created',
        default=1,
    )

    def __str__(self):
        """Course model string representation.

        Returns:
            str: Course title or 'Untitled Course' if title is empty.
        """
        return str(self.title) if self.title else 'Untitled Course'


class Enrollment(models.Model):
    """Model representing an enrollment of a user in a course."""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Meta class for Enrollment model."""

        unique_together = ('user', 'course')

    def __str__(self):
        """Enrollment model string representation.

        Returns:
            str: Enrollment information.
        """
        user_name = getattr(self.user, 'username', 'Unknown User')
        course_title = getattr(self.course, 'title', 'Unknown Course')
        return f'{user_name} enrolled in {course_title}'
