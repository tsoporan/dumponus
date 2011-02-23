from django.conf.urls.defaults import *

#from django.contrib.staticfiles.urls import staticfiles_urlpatterns
#urlpatterns += staticfiles_urlpatterns() 
## for django 1.3

from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'upload.views.upload', name="upload"),
    url(r'^list/$', 'upload.views.upload_list', name="upload-list"),
    url(r'^(?P<id>\d+)/$', 'upload.views.upload_detail', name="upload-detail"),
	url(r'^admin/', include(admin.site.urls), name="admin"),
)
