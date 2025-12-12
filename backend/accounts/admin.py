# backend/accounts/admin.py
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Register the default User model (if not already)
admin.site.unregister(User)
admin.site.register(User, BaseUserAdmin)
