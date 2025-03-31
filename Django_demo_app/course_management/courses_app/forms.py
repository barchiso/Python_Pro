"""Django form for course management."""
from django import forms

from .models import Course


class CourseForm(forms.ModelForm):
    """Form to add a new course."""

    class Meta:
        """Meta class for CourseForm."""

        model = Course
        fields = ['title', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }
