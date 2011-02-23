from django.contrib import admin
from upload.models import Upload 

class UploadAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'ip')

admin.site.register(Upload, UploadAdmin)
