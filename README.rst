django-gallery
==============

Simple gallery system for django.

Installation
------------

1. In your `settings.py`, add `gallery` to your `INSTALLED_APPS`.
2. Add `('gallery/', include('gallery.urls')),` to your `urls.py`
3. Sync your database


Settings
--------

+-----------------------------------+-----------------------------------+
| Setting                           | Default                           |
+===================================+===================================+
| GALLERY_STORAGE_PATH              | 'uploads/gallery/'                |
| GALLERY_AUTO_CLEANUP              | True                              |
| GALLERY_PHOTO_SOURCE_RESIZE       | '1600x1200'                       |
| GALLERY_NAME_FIELD_MAX_LENGTH     | 250                               |
| GALLERY_THUMBNAIL_MEDIA_URL       | THUMBNAIL_MEDIA_URL or MEDIA_URL  |
| GALLERY_PHOTO_VIEW_SIZE           | '700x450'                         |
| GALLERY_PHOTO_THUMBNAIL_SIZE      | '200x200'                         |
| GALLERY_PHOTO_MINI_THUMBNAIL_SIZE | '100x100'                         |
+-----------------------------------+-----------------------------------+


Credits
=======

This project was created and is sponsored by:

.. figure:: http://motion-m.ca/media/img/logo.png
    :figwidth: image

Motion Média (http://motion-m.ca)
