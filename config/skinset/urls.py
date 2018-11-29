from django.urls import path

from . import views

app_name = 'skinset'
urlpatterns = [
    path('', views.index, name='index'),
    path('list/<kind>/<int:identifier>', views.list, name='list'),
    path('crop/<int:identifier>', views.crop_image, name='crop_image'),
    path('img/<path:path>', views.image, name='img'),
]
