from django.db import models
from .user import User
from .upload import Upload

class PDFInfo(models.Model):
    upload = models.ForeignKey(Upload, on_delete=models.CASCADE, blank=False)
    #listOfMarks = models.JSONField()
    listOfSpans = models.JSONField()
    mark_id = models.IntegerField(blank=True, null=True)
    #Ideally, the comments should be referenced via mark_id. So you can select what comment to show via mark_id. 
    #This should probably be a many to many field for a comments object
    listOfComments = models.JSONField() #This should be a foreign key to a comment model? or something. I'm not sure what comments will be


