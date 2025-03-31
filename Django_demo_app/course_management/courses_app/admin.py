"""This file is used to register the models in the admin panel."""

from django.contrib import admin

from .models import Course


class CourseAdmin(admin.ModelAdmin):
    """Admin interface for Course model."""

    list_display = ('title', 'created_at', 'updated_at', 'created_by')
    search_fields = ('title', 'description')
    list_filter = ('created_at',)


admin.site.register(Course, CourseAdmin)
