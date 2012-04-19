from django.db import models

class Image(models.Model):
    #using for images currently, might extend later
    file = models.FileField(upload_to='images')
    created = models.DateTimeField(auto_now_add = True)
    ext = models.CharField(max_length=10)
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.file.url

    def url(self):
        return str(self.id) + self.ext
