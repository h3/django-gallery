from django.conf import settings

STORAGE_PATH  = getattr(settings, 'GALLERY_STORAGE_PATH', 'uploads/gallery/')

AUTO_CLEANUP  = getattr(settings, 'GALLERY_AUTO_CLEANUP', True)

SOURCE_RESIZE = getattr(settings, 'GALLERY_PHOTO_SOURCE_RESIZE', (1600, 1200))

NAME_FIELD_MAX_LENGTH = getattr(settings, 'GALLERY_NAME_FIELD_MAX_LENGTH', 250)

THUMBNAIL_MEDIA_URL  = getattr(settings, 'GALLERY_THUMBNAIL_MEDIA_URL', 
                        getattr(settings, 'THUMBNAIL_MEDIA_URL', 
                            getattr(settings, 'MEDIA_URL', )))
