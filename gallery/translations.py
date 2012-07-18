from modeltranslation.translator import translator, TranslationOptions
from gallery.models import Gallery, Photo, Zip


class GalleryTrans(TranslationOptions):
    fields = ('title','description' )
translator.register(Gallery, GalleryTrans)

class PhotoTrans(TranslationOptions):
    fields = ('title','caption',)
translator.register(Photo,PhotoTrans)

class ZipTrans(TranslationOptions):
    fields = ('title','description','caption')
translator.register(Zip,ZipTrans)
