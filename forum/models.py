from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from rallys import settings

class Topic(models.Model):
    title = models.CharField(max_length=70)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET('[Deleted]'))
    created_at = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.title

class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=datetime.now)
    parent_comment = models.ForeignKey('self', null = True, blank=True, on_delete = models.CASCADE, default = None)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.created_at}"