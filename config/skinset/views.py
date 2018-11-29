from PIL import Image
from django.shortcuts import HttpResponse
from django.shortcuts import render

from .models import ImageCategory, Skin, CropImage


def index(request):
    """
    indexのHttpResponseを返す.
    :param request: HttpRequest.
    :return: indexのHttpResponse.
    """
    image_categories = ImageCategory.objects.order_by('category')
    skins = Skin.objects.order_by('category')

    context = {
        'image_categories': image_categories,
        'skins': skins
    }
    return render(request, 'skinset/index.html', context)


def list(request, kind, identifier):
    """
    各一覧画面のHttpResponseを返す.
    :param request: HttpRequest.
    :param kind: 表示するデータ種別. 'image', 'skin'のいずれか.
    :param identifier: typeが'image'の場合はImageCategoryのID、'skin'の場合はSkinのID.
    :return: 一覧画面のHttpResponse.
    """
    context = {}

    if kind == 'image':
        context = {
            'image_list': CropImage.objects.filter(image_category=identifier).order_by('name'),
            'category_name': ImageCategory.objects.get(id=identifier).category
        }
    elif kind == 'skin':
        context = {
            'image_list': CropImage.objects.filter(skin=identifier).order_by('name'),
            'category_name': Skin.objects.get(id=identifier).name
        }
    else:
        pass

    return render(request, 'skinset/list.html', context)


def image(request, path):
    """
    指定したパスに格納されているファイルを画像として扱い、画像をHttpResponseとして返す.
    :param request: HttpRequest.
    :param path: ファイルパス. ui.ipfからの相対パスとして指定する.
    :return: 画像のHttpResponse.
    """
    im = Image.open('./static/skinset/ui.ipf/' + path)
    res = HttpResponse(content_type='image/png')
    im.save(res, 'PNG')
    return res


def crop_image(request, identifier):
    """
    指定したCropImageのIDに対応する画像をHttpResponseとして返す.
    :param request: HttpRequest.
    :param identifier: CropImageのID.
    :return: トリミング済み画像のHttpResponse.
    """
    record = CropImage.objects.filter(id=identifier)[0]

    l, t, w, h = [int(s) for s in record.imgrect.split()]
    im = Image.open('./static/skinset/ui.ipf/' + record.file)
    im = im.crop((l, t, (l + w), (t + h)))
    response = HttpResponse(content_type='image/png')
    im.save(response, 'PNG')

    return response
