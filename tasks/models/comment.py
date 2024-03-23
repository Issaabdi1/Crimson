"""comment.py"""
from django.db import models
from .user import User
from .upload import Upload
from datetime import datetime
from dateutil.relativedelta import relativedelta


class Comment(models.Model):
    upload = models.ForeignKey(Upload, on_delete=models.CASCADE, blank=False, null=False)
    mark_id = models.IntegerField(blank=True, null=True)
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    resolved = models.BooleanField(default=False)

    def __str__(self):
        return f"File {self.upload.file.name} is Comment by {self.commenter} on {self.date} with text: {self.text} in mark id: {self.mark_id}"

    def formatted_date(self):
        if not self.date:
            return "Date not set"
        now = datetime.now(self.date.tzinfo)
        delta = relativedelta(now, self.date)

        if delta.days == 0:
            return f"today {self.date.strftime('%H:%M')}"
        elif delta.days == 1:
            return f"yesterday {self.date.strftime('%H:%M')}"
        elif delta.days > 1 and delta.months == 0:
            return f"{delta.days} days ago"
        elif delta.months == 1:
            return "1 month ago"
        elif delta.months > 1:
            return f"{delta.months} months ago"