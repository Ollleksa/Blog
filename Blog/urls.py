from django.contrib import admin
from django.urls import path, include

from django.views.generic.base import TemplateView

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('blog/<int:blog_id>/', views.blog, name='blog'),
    path('message/<int:message_id>/', views.message, name='message'),
    path('blog/create_message', views.create, name='create_message'),
    path('create_blog', views.create_blog, name='create_blog'),
]
