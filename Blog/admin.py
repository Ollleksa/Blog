from django.contrib import admin

from .models import Blog, Message, Comment

admin.site.register(Blog)
admin.site.register(Message)
admin.site.register(Comment)
