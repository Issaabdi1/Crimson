"""comment.py"""
from django.db import models
from .user import User
from .upload import Upload


class Comment(models.Model):
    upload = models.ForeignKey(Upload, on_delete=models.CASCADE, blank=False, null=False)
    mark_id = models.IntegerField(blank=True, null=True)
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)
    text = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"File {self.upload.file.name} is Comment by {self.commenter} on {self.date} with text: {self.text} in mark id: {self.mark_id}"

