import re

from PIL import Image
from django.shortcuts import HttpResponse
from django.shortcuts import render

from .models import CropImage


def index(request):
    category_list = CropImage.objects \
        .values('category') \
        .order_by('category') \
        .distinct()
    context = {'category_list': category_list}
    return render(request, 'skinset/index.html', context)


def list(request, category_name):
    image_list = CropImage.objects.filter(category=category_name).order_by('file').all()
    context = {'category_name': category_name,
               'image_list': image_list}
    return render(request, 'skinset/list.html', context)


def img(request):
    im = Image.open('./static/ui.ipf/' + re.sub('^/skinset/img/', '', request.path))
    res = HttpResponse(content_type='image/png')
    im.save(res, 'PNG')
    return res


def dbimg(request, image_id):
    record = CropImage.objects.filter(id=image_id).all()[0]
    im = Image.open('./static/skinset/ui.ipf/' + record.file)
    l, t, w, h = [int(s) for s in record.imgrect.split()]
    im = im.crop((l, t, (l + w), (t + h)))
    res = HttpResponse(content_type='image/png')
    im.save(res, 'PNG')
    return res
