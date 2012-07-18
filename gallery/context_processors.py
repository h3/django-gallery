from itertools import chain

from gallery.models import Photo
from gallery.views import gallery_context

def latest_photos(request):
    return dict(chain(gallery_context.iteritems(), {
        'latest_photos': Photo.objects.order_by('?').filter(is_visible=True)[0:4]
    }.iteritems()))

