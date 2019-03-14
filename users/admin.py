from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin

from .models import BlogUser
from .forms import BlogUserCreationForm, BlogUserChangeForm

class BlogUserAdminView(UserAdmin):
    add_form = BlogUserCreationForm
    form = BlogUserChangeForm
    model = BlogUser
    list_display = ('username', 'email', 'first_name', 'last_name', 'phone', 'is_verified')

    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'phone')}),
        ('Permissions', {'fields': ('is_verified',)}),
    )

    add_fieldsets = (
        (None, {'fields': ('username', 'email', 'password1', 'password2')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'phone')}),
        ('Permissions', {'fields': ('is_verified',)}),
    )

admin.site.register(BlogUser, BlogUserAdminView)
admin.site.unregister(Group)