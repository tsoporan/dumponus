from django import forms
from django.forms import ModelForm
from upload.models import Upload
import os
from django.http import HttpResponse

class UploadForm(ModelForm):
    class Meta:
        model = Upload
        fields = ('name', 'upload', 'tags')

    def __init__(self, *args, **kwargs):
        super(UploadForm, self).__init__(*args, **kwargs)
        for field in self.fields.keys():
            self.fields[field].widget.attrs['placeholder'] = self.fields[field].help_text
    
    def clean_upload(self):
        upload = self.cleaned_data['upload']
        fname, ext = os.path.splitext(upload.name) 
        image = [".png", ".jpg", ".jpeg", ".tiff", ".bmp", ".gif"]
        video = [".ogg",]
        if not ext.lower() in image and not ext.lower() in video:
            raise forms.ValidationError("Upload must be an image or video.")
        return upload
