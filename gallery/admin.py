# -*- coding: utf-8 -*-

from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

from easy_thumbnails.files import get_thumbnailer
from gallery.models import Gallery, Photo, Zip
from gallery.conf import settings

try:
    from grappellifit.admin import TranslationAdmin
    from modeltranslation.admin import TranslationStackedInline
    BaseClass = TranslationAdmin
    StackedBaseClass = TranslationStackedInline
except:
    try:
        from modeltranslation.admin import TranslationAdmin,\
                                            TranslationStackedInline
        BaseClass = TranslationAdmin
        StackedBaseClass = TranslationStackedInline
    except:
        BaseClass = admin.ModelAdmin
        StackedBaseClass = admin.StackedInline


def admin_photo_thumbnail(source):
    thumbnail_options = dict(size=(80, 80), crop='smart')
    return get_thumbnailer(source).get_thumbnail(thumbnail_options)


class PhotoAdminInline(StackedBaseClass):
    model = Photo
    extra = 1
    allow_add = True
    fk_name = 'gallery'
    classes = ('collapse open',)


class GalleryAdmin(BaseClass):
    list_display = ('__unicode__', 'get_photo_count', 'date_created', 'weight')
    list_editable = ('weight',)
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [PhotoAdminInline, ]
    list_filter = ('is_visible',)
    date_hierarchy = 'date_created'

    def get_photo_count(self, inst):
        count = len(inst.photo_set.all())
        link = '<a href="../photo/?gallery__id__exact=%d">%d</a>'
        return link % (inst.pk, count)
    get_photo_count.allow_tags = True
    get_photo_count.short_description = _('Photos')

admin.site.register(Gallery, GalleryAdmin)


class PhotoAdmin(BaseClass):
    list_display = ('__unicode__', 'date_created', 'gallery', 'weight',\
                    'get_admin_photo')
    list_editable = ('weight',)
    list_filter = ('gallery', 'is_visible')
    search_fields = ('title', 'caption')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'date_created'

    def get_admin_photo(self, inst):
        if inst.image:
            src = (settings.THUMBNAIL_MEDIA_URL,\
                    admin_photo_thumbnail(inst.image))
            return mark_safe('<img src="%s%s" />' % src)
        else:
            return _('No photo')
    get_admin_photo.allow_tags = True
    get_admin_photo.short_description = _('Photo')

admin.site.register(Photo, PhotoAdmin)


class ZipAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}
admin.site.register(Zip, ZipAdmin)
