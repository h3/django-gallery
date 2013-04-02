from django.conf.urls.defaults import patterns, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'gallery.views.gallery_list', name='gallery-list'),

    url(r'^(?P<gallery_slug>[\-\d\w]+)/$',
        'gallery.views.gallery_detail', name='gallery-detail'),

    url(r'^(?P<gallery_slug>[\-\d\w]+)/photo/(?P<photo_slug>[\-\d\w]+)$',
        'gallery.views.photo_detail', name='gallery-photo-detail'),
)
