from django.urls import path, re_path

from . import views

app_name = 'skinset'
urlpatterns = [
    path('', views.index, name='index'),
    path('category/<category_name>', views.list, name='list'),
    path('dbimg/<int:image_id>', views.dbimg, name='dbimg'),
    re_path(r'^.*.tga$', views.img, name='img'),
]
