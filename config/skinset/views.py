import re

from PIL import Image
from django.shortcuts import HttpResponse
from django.shortcuts import render

from .models import CropImage, SkinImage


def index(request):
    category_list = CropImage.objects \
        .values('category') \
        .order_by('category') \
        .distinct()
    skin_list = SkinImage.objects\
        .values('skin_category') \
        .order_by('skin_category') \
        .distinct()
    context = {
        'category_list': category_list,
        'skin_list': skin_list
    }
    return render(request, 'skinset/index.html', context)


def list_image(request, category_name):
    image_list = CropImage.objects.filter(category=category_name).order_by('file').all()
    context = {'category_name': category_name,
               'image_list': image_list}
    return render(request, 'skinset/list_image.html', context)


def list_skin(request, category_name):
    image_list = SkinImage.objects.filter(skin_category=category_name).order_by('skin_name').all()
    context = {'category_name': category_name,
               'image_list': image_list}
    return render(request, 'skinset/list_skin.html', context)


def img(request):
    im = Image.open('./static/ui.ipf/' + re.sub('^/skinset/img/', '', request.path))
    res = HttpResponse(content_type='image/png')
    im.save(res, 'PNG')
    return res


def img_image(request, image_id):
    record = CropImage.objects.filter(id=image_id).all()[0]
    return crop_img(request, record.file, record.imgrect)


def img_skin(request, skin_id):
    record = SkinImage.objects.filter(id=skin_id).all()[0]
    return crop_img(request, record.texture, record.imgrect)


def crop_img(request, file, rect):
    l, t, w, h = [int(s) for s in rect.split()]
    im = Image.open('./static/skinset/ui.ipf/' + file)
    im = im.crop((l, t, (l + w), (t + h)))
    res = HttpResponse(content_type='image/png')
    im.save(res, 'PNG')
    return res
