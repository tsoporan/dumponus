from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'upload.views.upload', name='upload'),
    url(r'^(?P<id>\d+)/$', 'upload.views.detail', name='detail'),
    url(r'^(?P<id>\d+)\.(?P<ext>\w+)$', 'upload.views.detail', name='detail_raw'),
    url(r'^admin/', include(admin.site.urls)),
)

#for development only
if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
        url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.STATIC_ROOT,
        }),
   )
