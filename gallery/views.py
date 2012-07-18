# Create your views here.
from django.conf import settings
from django.template import Context, loader, RequestContext
from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response, get_object_or_404

from gallery.models import Photo,Gallery

PHOTO_VIEW_SIZE = getattr(settings, 'GALLERY_PHOTO_VIEW_SIZE', '700x450')
PHOTO_THUMBNAIL_SIZE = getattr(settings, 'GALLERY_PHOTO_THUMBNAIL_SIZE', '200x200')
PHOTO_MINI_THUMBNAIL_SIZE = getattr(settings, 'GALLERY_PHOTO_MINI_THUMBNAIL_SIZE', '100x100')

gallery_context = {
    'mini_thumb_size': PHOTO_MINI_THUMBNAIL_SIZE,
    'thumb_size': PHOTO_THUMBNAIL_SIZE,
    'photo_size': PHOTO_VIEW_SIZE,
}

def gallery_list(request):
    gallery_context.update({
        'object_list': Gallery.objects.filter(is_visible=True),
        'recent_photos': Photo.objects.filter(is_visible=True)[0:10],
    })
    return render_to_response('gallery/gallery_list.html', gallery_context, 
            context_instance=RequestContext(request))


def gallery_detail(request, gallery_slug):
    gallery_object = get_object_or_404(Gallery, slug=gallery_slug)
    gallery_context.update({
        'object': gallery_object,
        'gallery_list': Gallery.objects.filter(is_visible=True),
    })
    return render_to_response('gallery/gallery_detail.html', gallery_context, 
            context_instance=RequestContext(request))

def photo_detail(request, gallery_slug,photo_slug):
    photo_object= get_object_or_404(Photo, slug=photo_slug)
    gallery_context.update({
        'photo': photo_object,
        'gallery_list': Gallery.objects.filter(is_visible=True),
    })
    return render_to_response('gallery/photo_detail.html', gallery_context, 
            context_instance=RequestContext(request))

