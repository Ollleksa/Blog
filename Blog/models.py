from django.db import models
from users.models import BlogUser


class Blog(models.Model):
    name = models.CharField(max_length = 40, unique = True)
    user = models.ForeignKey(BlogUser, on_delete = models.CASCADE)

    def __str__(self):
        return self.name


class Message(models.Model):
    name = models.CharField(max_length = 100)
    blog = models.ForeignKey(Blog, on_delete = models.CASCADE)
    content = models.TextField(blank=True, default='')
    timestamp = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.name


class Comment(models.Model):
    user = models.ForeignKey(BlogUser, on_delete = models.CASCADE)
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now = True)
    content = models.TextField(blank=True, default='')

    def __str__(self):
        des = '{0} commented {1}'.format(self.user.username, self.message.name)
        return des