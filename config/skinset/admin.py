from django.contrib import admin

from .models import ImageCategory, SkinCategory, Skin, CropImage

admin.site.register(ImageCategory)
admin.site.register(SkinCategory)
admin.site.register(Skin)
admin.site.register(CropImage)
