"""This file is used to register the models in the admin panel."""
from django.contrib import admin
from accounts.models import CustomUser


admin.site.register(CustomUser)
