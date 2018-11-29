from django.db import models


class ImageCategory(models.Model):
    category = models.CharField(max_length=128)

    def __str__(self):
        return self.category


class SkinCategory(models.Model):
    category = models.CharField(max_length=128)

    def __str__(self):
        return self.category


class Skin(models.Model):
    name = models.CharField(max_length=128)
    category = models.ForeignKey('SkinCategory', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class CropImage(models.Model):
    name = models.CharField(max_length=128)
    imgrect = models.CharField(max_length=64)
    file = models.CharField(max_length=256)
    source_path = models.CharField(max_length=256)
    image_category = models.ForeignKey('ImageCategory', on_delete=models.CASCADE, null=True)
    skin = models.ForeignKey('Skin', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name
