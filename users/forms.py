from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import BlogUser

class BlogUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = BlogUser
        fields = ('username', 'email', 'first_name', 'last_name', 'phone')

class BlogUserChangeForm(UserChangeForm):

    class Meta:
        model = BlogUser
        fields = ('username', 'email', 'first_name', 'last_name', 'phone', 'is_verified')
