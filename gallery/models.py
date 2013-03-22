import os
import zipfile
import Image

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import smart_str, force_unicode
from django.core.urlresolvers import reverse
from django.core.files.base import ContentFile
from django.template.defaultfilters import slugify

from gallery.conf import settings
from easy_thumbnails.fields import ThumbnailerImageField


class Gallery(models.Model):
    title = models.CharField(_('Title'), max_length=settings.NAME_FIELD_MAX_LENGTH, unique=True)
    slug = models.SlugField(_('Slug'), max_length=settings.NAME_FIELD_MAX_LENGTH, unique=True, help_text=_('A "slug" is a unique URL-friendly title for an object.'))
    description = models.TextField(_('Description'), blank=True)
    is_visible = models.BooleanField(_('Is visible'), default=True, help_text=_('If true, the gallery will be displayed on the website'))
    date_created = models.DateTimeField(_('Date created'), auto_now_add=True)

    def get_random_photos(self):
        return self.photo_set.all().order_by('?')

    def get_absolute_url(self):
        return reverse('gallery-detail', args=[self.slug])

    def __unicode__(self):
        if self.title:
            return u'%s' % self.title
        elif hasattr(self, 'title_fr') and self.title_fr:
            return u'%s' % self.title_fr
        elif hasattr(self, 'title_en') and self.title_en:
            return u'%s' % self.title_en


    class Meta:
        ordering = ('date_created',)
        verbose_name = _('Gallery')
        verbose_name_plural = _('Galleries')


class Photo(models.Model):
    title      = models.CharField(_('Photo'),max_length=settings.NAME_FIELD_MAX_LENGTH, unique=True)
    slug       = models.SlugField(_('Slug'),max_length=settings.NAME_FIELD_MAX_LENGTH, unique=True, help_text=_('A "slug" is a unique URL-friendly title for an object.'))
    caption    = models.TextField(_('Caption'), blank=True)
    gallery    = models.ForeignKey(Gallery, null=True, blank=True)
    image      = ThumbnailerImageField(_('Image'), upload_to=settings.STORAGE_PATH, resize_source=dict(size=settings.SOURCE_RESIZE))
    is_visible = models.BooleanField(_('Visible on website'), default=True)
    date_created = models.DateTimeField(_('Date created'), auto_now_add=True)

    def get_absolute_url(self):
        return reverse('gallery-photo-detail', args=[self.gallery.slug, self.slug])

    def get_previous_in_gallery(self):
        try:
            return self.get_previous_by_date_created(gallery__exact=self.gallery, is_visible=True)
        except Photo.DoesNotExist:
            return None

    def get_next_in_gallery(self):
        try:
            return self.get_next_by_date_created(gallery__exact=self.gallery, is_visible=True)
        except Photo.DoesNotExist:
            return None

    def __unicode__(self):
        if self.title:
            return u'%s' % self.title
        elif hasattr(self, 'title_fr') and self.title_fr:
            return u'%s' % self.title_fr
        elif hasattr(self, 'title_en') and self.title_en:
            return u'%s' % self.title_en

    class Meta:
        ordering = ('date_created', '-id',)
        verbose_name = _('Photo')
        verbose_name_plural = _('Photos')
        get_latest_by = 'date_created'

if settings.AUTO_CLEANUP:
    from django.db.models.signals import post_delete
    from gallery.utils import file_cleanup
    post_delete.connect(file_cleanup, sender=Photo, dispatch_uid="photo.file_cleanup")


class Zip(models.Model):
    title = models.CharField(_('Title'), max_length=75, help_text=_('All photos in the gallery will be given a title made up of the gallery title + a sequential number.'))
    slug = models.CharField(_('Slug'),max_length=settings.NAME_FIELD_MAX_LENGTH, unique=True, help_text=_('A "slug" is a unique URL-friendly title for an object.'))
    description = models.TextField(_('Description'), blank=True)
    caption = models.TextField(_('Caption'), blank=True)
    visible = models.BooleanField(_('Is visible'), default=True, help_text=_('If true, the photo will be display in de view'))
    gallery = models.ForeignKey(Gallery, null=True, blank=True, help_text=_('Select the gallery that the Photo have to be link '))
    zip_file = models.FileField(_('images file (.zip)'), upload_to=settings.STORAGE_PATH+"/tmp",help_text=_('Select a .zip file of images to upload into a new Gallery.'))

    def save(self, *args, **kwargs):
        super(Zip, self).save(*args, **kwargs) 
        gallery = self.process_zipfile()
        super(Zip, self).delete()
        return gallery

    def process_zipfile(self):
        if os.path.isfile(self.zip_file.path):
            try:
                # TODO: implement try-except here
                zip = zipfile.ZipFile(self.zip_file.path)
                bad_file = zip.testzip()
                if bad_file:
                    raise Exception('"%s" in the .zip archive is corrupt.' % bad_file)
                count = 1
                if self.gallery:
                    gallery = self.gallery
                else:
                    gallery = Gallery.objects.create(title=self.title,
                                                     title_slug=slugify(self.title),
                                                     description=self.description,)
                from cStringIO import StringIO
                for filename in sorted(zip.namelist()):
                    if filename.startswith('__'): # do not process meta files
                        continue
                    data = zip.read(filename)
                    if len(data):
                        try:
                            # the following is taken from django.newforms.fields.ImageField:
                            #  load() is the only method that can spot a truncated JPEG,
                            #  but it cannot be called sanely after verify()
                            trial_image = Image.open(StringIO(data))
                            trial_image.load()
                            # verify() is the only method that can spot a corrupt PNG,
                            #  but it must be called immediately after the constructor
                            trial_image = Image.open(StringIO(data))
                            trial_image.verify()
                        except Exception:
                            # if a "bad" file is found we just skip it.
                            count+=1
                            continue
                        while 1:
                            _title = ' '.join([self.title, str(count)])
                            _slug = self.slug+"_"+str(count)
                            try:
                                p = Photo.objects.get(slug=_slug)
                            except Photo.DoesNotExist:
                                print(_slug)
                                photo = Photo(title=_title,
                                              slug=_slug,
                                              caption=self.caption,
                                              is_visible=self.visible,
                                              gallery=self.gallery,)
                                #img= Image.open(StringIO(data))
                                photo.image.save(filename,ContentFile(data))
                                #gallery.photos.add(photo)
                                count +=1
                                break
                            count +=1
                zip.close()
                os.remove(self.zip_file.path)
                return gallery
            except:
                os.remove(self.zip_file.path)


    class Meta:
        verbose_name = _('Zip photo upload')
        verbose_name_plural = _('Zip photo uploads')
