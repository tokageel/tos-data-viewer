from django.urls import path, re_path

from . import views

app_name = 'skinset'
urlpatterns = [
    path('', views.index, name='index'),
    path('list/image/<category_name>', views.list_image, name='list_image'),
    path('list/skin/<category_name>', views.list_skin, name='list_skin'),
    path('img/image/<int:image_id>', views.img_image, name='img_image'),
    path('img/skin/<int:skin_id>', views.img_skin, name='img_skin'),
    re_path(r'^.*.tga$', views.img, name='img'),
]
