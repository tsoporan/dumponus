from django.db import models
from upload.utils import randoName, randThumbSize, generateThumb
from django.template import defaultfilters
from tagging.fields import TagField
import datetime
import os

def checkExt(filename):
    """Simply return 'video' or 'image' depending on the extension of the file."""
    fname, ext = os.path.splitext(filename)
    image = [".png", ".jpg", ".jpeg", ".tiff", ".bmp", ".gif"]
    video = [".ogg",]
    if ext.lower() in image: return "image"
    if ext.lower() in video: return "video"

class Upload(models.Model):
    
    TYPES = (
        ('video', 'video'),
        ('image', 'image'),
    )
    
    name = models.CharField(max_length=255, help_text="name of upload")
    upload = models.FileField(upload_to='uploads',  help_text="the file")
    tags = TagField('Tags', help_text="awesome, fun, cool")
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    ip = models.IPAddressField(blank=True, null=True)
    type = models.CharField(max_length=100, choices=TYPES, blank=True, null=True)

    def __unicode__(self):
        return self.name   

    def save(self, *args, **kwargs):
        """Check file extenision to determine type on save."""
        if not self.type:
            self.type = checkExt(self.upload.file.name)
        super(Upload, self).save(*args, **kwargs)
