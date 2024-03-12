"""comment.py"""
from django.db import models
from .user import User
from .upload import Upload


class Comment(models.Model):
    mark_id = models.IntegerField(blank=True, null=True)
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)
    text = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Comment by {self.commenter} on {self.date} with text {self.text} in {self.mark_id}"